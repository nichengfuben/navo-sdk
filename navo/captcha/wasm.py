from __future__ import annotations

import asyncio
import logging
import shutil
import subprocess
import time
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional

import requests

from navo.captcha.nodescript import NODE_SCRIPT
from navo.captcha.solve import _solve_python

_logger = logging.getLogger("navo.captcha")
_DEFAULT_ORIGIN = "https://navo.airoe.cn"
_TIMEOUT = 15
_WASM_CDN_BASE = "https://cdn.jsdelivr.net/npm/@cap.js/wasm@0.0.6/browser/"
_WASM_JS_FILE = "cap_wasm.min.js"
_WASM_BINARY_FILE = "cap_wasm_bg.wasm"
_NODE_SCRIPT_NAME = "_cap_solver.mjs"
_CACHE_DIR = Path(__file__).resolve().parent / "_wasm_cache"


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
