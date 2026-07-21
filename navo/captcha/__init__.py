"""Captcha solver public API."""

from navo.captcha.wasm import asolve_captcha, solve_captcha_sync, solve_captcha_wasm_sync

__all__ = ["asolve_captcha", "solve_captcha_sync", "solve_captcha_wasm_sync"]
