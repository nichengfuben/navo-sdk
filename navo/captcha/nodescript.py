"""Embedded Node.js WASM solver script."""

NODE_SCRIPT = r'''\
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
'''
