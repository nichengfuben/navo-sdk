from __future__ import annotations

import hashlib


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


__all__ = ["_solve_one", "_solve_worker"]
