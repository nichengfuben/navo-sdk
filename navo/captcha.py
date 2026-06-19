"""
CapWorker proof-of-work captcha solver for Navo IM.

Provides both synchronous and asynchronous entry points.
Tries a pure-Python solver first, falling back to the official
cap.js WASM module executed via a Node.js subprocess.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import multiprocessing
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional

import requests

_logger = logging.getLogger("navo.captcha")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_DEFAULT_ORIGIN = "https://navo.airoe.cn"
_TIMEOUT = 15  # seconds for HTTP requests

_WASM_CDN_BASE = "https://cdn.jsdelivr.net/npm/@cap.js/wasm@0.0.6/browser/"
_WASM_JS_FILE = "cap_wasm.min.js"
_WASM_BINARY_FILE = "cap_wasm_bg.wasm"
_NODE_SCRIPT_NAME = "_cap_solver.mjs"

# Cache WASM assets inside the package directory.
_CACHE_DIR = Path(__file__).resolve().parent / "_wasm_cache"

# ---------------------------------------------------------------------------
# CapWorker PRNG (FNV-1a seed + xorshift32)
# ---------------------------------------------------------------------------


def _fnv1a(text: str) -> int:
    """FNV-1a 32-bit hash used to seed the PRNG."""
    h = 2166136261
    for ch in text:
        h ^= ord(ch)
        h = (h + ((h << 1) & 0xFFFFFFFF)
                 + ((h << 4) & 0xFFFFFFFF)
                 + ((h << 7) & 0xFFFFFFFF)
                 + ((h << 8) & 0xFFFFFFFF)
                 + ((h << 24) & 0xFFFFFFFF)) & 0xFFFFFFFF
    return h


def _xorshift32(state: int) -> int:
    """Xorshift32 step."""
    state ^= (state << 13) & 0xFFFFFFFF
    state ^= (state >> 17) & 0xFFFFFFFF
    state ^= (state << 5) & 0xFFFFFFFF
    return state & 0xFFFFFFFF


def prng_string(seed: str, length: int) -> str:
    """Generate a deterministic pseudo-random hex string of given length."""
    state = _fnv1a(seed)
    result = ""
    while len(result) < length:
        state = _xorshift32(state)
        result += format(state, "08x")
    return result[:length]


# ---------------------------------------------------------------------------
# Proof-of-work solver (pure Python)
# ---------------------------------------------------------------------------


def _solve_one(salt: str, target_hex: str) -> int:
    """Find nonce such that SHA-256(salt + str(nonce)) starts with target bytes."""
    target_bytes = bytes.fromhex(target_hex)
    n = len(target_bytes)
    nonce = 0
    while True:
        data = f"{salt}{nonce}".encode("utf-8")
        digest = hashlib.sha256(data).digest()
        if digest[:n] == target_bytes:
            return nonce
        nonce += 1


def _solve_worker(args: tuple) -> int:
    """Worker wrapper for parallel solving."""
    salt, target_hex = args
    return _solve_one(salt, target_hex)


def _solve_python(pow_url: str, workers: int) -> Optional[str]:
    """Full captcha flow using the pure-Python PoW solver.

    Returns the redeemed captcha token, or None if the server rejected it.
    """
    session = requests.Session()
    session.headers.update({
        "Origin": _DEFAULT_ORIGIN,
        "Referer": f"{_DEFAULT_ORIGIN}/",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
    })

    # Step 1: Get challenge
    _logger.debug("Requesting captcha challenge...")
    resp = session.post(f"{pow_url}/api/challenge", timeout=_TIMEOUT)
    resp.raise_for_status()
    body = resp.json()

    challenge = body["challenge"]  # { c: int, s: int, d: int }
    token = body["token"]
    c_count = challenge["c"]
    s_len = challenge["s"]
    d_len = challenge["d"]

    _logger.debug("Challenge: c=%d, s=%d, d=%d", c_count, s_len, d_len)

    # Step 2: Expand challenges into (salt, target) pairs
    challenges = []
    for t in range(1, c_count + 1):
        salt = prng_string(f"{token}{t}", s_len)
        target = prng_string(f"{token}{t}d", d_len)
        challenges.append((salt, target))

    # Step 3: Solve all challenges in parallel
    _logger.info("Solving %d captcha challenges with %d workers...", c_count, workers)
    t0 = time.monotonic()
    solutions = [0] * c_count

    # On Windows, freeze_support() is needed so that frozen executables (and
    # spawn-based child processes) do not re-run the top-level import block.
    multiprocessing.freeze_support()

    executor = ProcessPoolExecutor(max_workers=workers)
    try:
        future_to_idx = {}
        for idx, chal in enumerate(challenges):
            fut = executor.submit(_solve_worker, chal)
            future_to_idx[fut] = idx

        solved = 0
        for fut in as_completed(future_to_idx):
            idx = future_to_idx[fut]
            solutions[idx] = fut.result()
            solved += 1
            if solved % 10 == 0 or solved == c_count:
                _logger.debug("Solved %d/%d", solved, c_count)
    except KeyboardInterrupt:
        # Cancel pending futures and stop waiting for results immediately.
        executor.shutdown(wait=False, cancel_futures=True)
        # On Windows (spawn start method), child processes re-import the
        # main module.  If they receive SIGINT during import they emit
        # massive traceback spam.  Force-terminate every active child.
        for child in multiprocessing.active_children():
            try:
                child.terminate()
            except Exception:
                pass
        raise
    except Exception:
        executor.shutdown(wait=False)
        raise
    else:
        executor.shutdown(wait=True)

    elapsed = time.monotonic() - t0
    _logger.debug("All challenges solved in %.1fs", elapsed)

    # Step 4: Redeem token
    _logger.debug("Redeeming captcha token...")
    redeem_body = {"token": token, "solutions": solutions}
    resp = session.post(
        f"{pow_url}/api/redeem",
        json=redeem_body,
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    redeem_data = resp.json()

    if not redeem_data.get("success"):
        _logger.warning("Python solver redeem rejected: %s", redeem_data)
        return None

    captcha_token = redeem_data["token"]
    _logger.info("Captcha token redeemed successfully.")
    return captcha_token


# ---------------------------------------------------------------------------
# WASM fallback -- downloads official cap.js WASM and solves via Node.js
# ---------------------------------------------------------------------------

_NODE_SCRIPT = r"""\
// Auto-generated Node.js wrapper for cap.js WASM captcha solver.
// Requires Node.js >= 18 (native fetch).
// Uses the official cap.js WASM glue code (cap_wasm.min.js) for WASM init.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { createHash } from "node:crypto";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ------------------------------------------------------------------
// Load the official cap.js WASM module via its JS glue code.
// cap_wasm.min.js exports: initSync, solve_pow (and default init)
// ------------------------------------------------------------------
import { initSync, solve_pow as wasmSolvePow } from "./cap_wasm.min.js";

let wasmReady = false;
try {
  const wasmBytes = readFileSync(join(__dirname, "cap_wasm_bg.wasm"));
  initSync(wasmBytes);
  wasmReady = true;
  console.error("[wasm] WASM module initialized successfully");
} catch (err) {
  console.error("[wasm] WASM init failed:", err.message, "- will use JS fallback");
}

// ------------------------------------------------------------------
// PRNG helpers (FNV-1a seed + xorshift32) -- mirrors the Python impl
// ------------------------------------------------------------------
function fnv1a(text) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h;
}

function xorshift32(state) {
  state ^= (state << 13) >>> 0;
  state ^= (state >>> 17);
  state ^= (state << 5) >>> 0;
  return state >>> 0;
}

function prngString(seed, length) {
  let state = fnv1a(seed);
  let result = "";
  while (result.length < length) {
    state = xorshift32(state);
    result += state.toString(16).padStart(8, "0");
  }
  return result.slice(0, length);
}

// ------------------------------------------------------------------
// JS fallback PoW solver (SHA-256 brute force)
// ------------------------------------------------------------------
function sha256(data) {
  return createHash("sha256").update(data).digest();
}

function solvePowJS(salt, targetHex) {
  const targetBytes = Buffer.from(targetHex, "hex");
  const n = targetBytes.length;
  let nonce = 0;
  while (true) {
    const data = salt + nonce;
    const digest = sha256(data);
    if (digest.subarray(0, n).equals(targetBytes)) return nonce;
    nonce++;
  }
}

function solvePow(salt, targetHex) {
  if (wasmReady) {
    try {
      const result = wasmSolvePow(salt, targetHex);
      return Number(result);
    } catch (err) {
      console.error("[wasm] WASM solve_pow failed:", err.message, "- using JS fallback");
      wasmReady = false;
    }
  }
  return solvePowJS(salt, targetHex);
}

// ------------------------------------------------------------------
// Main flow: challenge -> solve -> redeem
// ------------------------------------------------------------------
const POW_URL = process.argv[2];
const headers = {
  "Content-Type": "application/json",
  "Origin": "https://navo.airoe.cn",
  "Referer": "https://navo.airoe.cn/",
  "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) " +
    "Chrome/151.0.0.0 Safari/537.36",
};

// 1) Get challenge
const chalResp = await fetch(POW_URL + "/api/challenge", {
  method: "POST",
  headers,
});
if (!chalResp.ok) {
  console.error("Challenge request failed:", chalResp.status);
  process.exit(1);
}
const chalBody = await chalResp.json();
const { challenge, token } = chalBody;
const { c: cCount, s: sLen, d: dLen } = challenge;

console.error(`[wasm] Challenge: c=${cCount}, s=${sLen}, d=${dLen}`);
console.error(`[wasm] Token: ${token}`);

// 2) Expand and solve
const t0 = Date.now();
const solutions = [];
for (let t = 1; t <= cCount; t++) {
  const salt = prngString(`${token}${t}`, sLen);
  const target = prngString(`${token}${t}d`, dLen);
  solutions.push(solvePow(salt, target));
  if (t % 10 === 0 || t === cCount) {
    console.error(`[wasm] Solved ${t}/${cCount}`);
  }
}
const elapsed = (Date.now() - t0) / 1000;
console.error(`[wasm] All challenges solved in ${elapsed.toFixed(1)}s`);

// 3) Redeem
const redeemResp = await fetch(POW_URL + "/api/redeem", {
  method: "POST",
  headers,
  body: JSON.stringify({ token, solutions }),
});
if (!redeemResp.ok) {
  console.error("Redeem request failed:", redeemResp.status);
  process.exit(1);
}
const redeemBody = await redeemResp.json();
if (!redeemBody.success) {
  console.error("Redeem rejected:", JSON.stringify(redeemBody));
  process.exit(1);
}

// Output only the token on stdout (everything else goes to stderr)
process.stdout.write(redeemBody.token);
"""


def _ensure_wasm_files() -> Path:
    """Download and cache the cap.js WASM assets if not already present.

    Returns the cache directory path containing the files.
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)

    for filename in (_WASM_JS_FILE, _WASM_BINARY_FILE):
        dest = _CACHE_DIR / filename
        if dest.exists() and dest.stat().st_size > 0:
            continue
        url = _WASM_CDN_BASE + filename
        _logger.info("Downloading WASM asset: %s", url)
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        _logger.debug("Saved %s (%d bytes)", dest, len(resp.content))

    return _CACHE_DIR


def _write_node_script() -> Path:
    """Write the Node.js WASM solver script to the cache directory."""
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    script_path = _CACHE_DIR / _NODE_SCRIPT_NAME
    script_path.write_text(_NODE_SCRIPT, encoding="utf-8")
    return script_path


def solve_captcha_wasm_sync(pow_url: str) -> str:
    """Solve the captcha using the official cap.js WASM module via Node.js.

    Downloads the WASM assets if not cached, writes a small Node.js driver
    script, and invokes it as a subprocess.  The Node.js script performs the
    full challenge -> solve -> redeem flow and prints the resulting token
    to stdout.

    Raises RuntimeError if Node.js is not found or the subprocess fails.
    """
    node_bin = shutil.which("node")
    if node_bin is None:
        raise RuntimeError(
            "Node.js not found on PATH. Install Node.js >= 18 for WASM fallback."
        )

    _ensure_wasm_files()
    script_path = _write_node_script()

    _logger.info("Running Node.js WASM captcha solver...")
    try:
        result = subprocess.run(
            [node_bin, str(script_path), pow_url],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(_CACHE_DIR),
        )
    except KeyboardInterrupt:
        raise  # User is shutting down, don't fall back or wrap
    except subprocess.TimeoutExpired:
        raise RuntimeError("WASM solver timed out after 120 seconds")

    # Forward stderr for visibility
    if result.stderr:
        for line in result.stderr.splitlines():
            _logger.debug("[wasm] %s", line)

    if result.returncode != 0:
        raise RuntimeError(
            f"WASM solver exited with code {result.returncode}\n"
            f"stderr: {result.stderr}"
        )

    token = result.stdout.strip()
    if not token:
        raise RuntimeError("WASM solver produced no token")

    _logger.info("WASM captcha token redeemed successfully.")
    return token


# ---------------------------------------------------------------------------
# Orchestrator -- Python first, WASM fallback (sync)
# ---------------------------------------------------------------------------


def solve_captcha_sync(pow_url: str, workers: Optional[int] = None) -> str:
    """Solve the captcha synchronously, trying the pure-Python solver first.

    If the Python solver fails (exception or server rejection), the official
    cap.js WASM module is used via a Node.js subprocess as a fallback.

    Parameters
    ----------
    pow_url : str
        Base URL of the PoW captcha service (e.g. ``https://pow.airoe.cn``).
    workers : int, optional
        Number of parallel processes for the Python solver
        (defaults to ``min(cpu_count(), 50)``).

    Returns
    -------
    str
        The redeemed captcha token ready for the login request.
    """
    workers = workers or min(cpu_count(), 50)

    # --- Primary: pure-Python solver ---
    try:
        result = _solve_python(pow_url, workers)
        if result:
            return result
        _logger.info("Python solver returned None, falling back to WASM...")
    except KeyboardInterrupt:
        raise  # User is shutting down, don't fall back to WASM
    except Exception as exc:
        _logger.warning("Python solver failed: %s, falling back to WASM...", exc)

    # --- Fallback: WASM via Node.js ---
    return solve_captcha_wasm_sync(pow_url)


# ---------------------------------------------------------------------------
# Async wrappers
# ---------------------------------------------------------------------------


async def solve_captcha(pow_url: str, workers: Optional[int] = None) -> str:
    """Async wrapper around :func:`solve_captcha_sync` using ``asyncio.to_thread``."""
    return await asyncio.to_thread(solve_captcha_sync, pow_url, workers)


async def asolve_captcha(pow_url: str, workers: Optional[int] = None) -> str:
    """Alias for :func:`solve_captcha` (async)."""
    return await asyncio.to_thread(solve_captcha_sync, pow_url, workers)


__all__ = [
    "solve_captcha_sync",
    "solve_captcha_wasm_sync",
    "solve_captcha",
    "asolve_captcha",
    "prng_string",
]
