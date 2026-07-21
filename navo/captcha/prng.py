from __future__ import annotations

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


__all__ = ["_fnv1a", "_xorshift32", "prng_string"]
