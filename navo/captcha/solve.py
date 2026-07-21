from __future__ import annotations

import logging
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional

import requests

from navo.captcha.pow import _solve_worker
from navo.captcha.prng import prng_string

_logger = logging.getLogger("navo.captcha")
_DEFAULT_ORIGIN = "https://navo.airoe.cn"
_TIMEOUT = 15


def _captcha_session() -> requests.Session:
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
    return session


def _fetch_challenge(session: requests.Session, pow_url: str) -> tuple[dict, str, int, int, int]:
    _logger.debug("Requesting captcha challenge...")
    resp = session.post(f"{pow_url}/api/challenge", timeout=_TIMEOUT)
    resp.raise_for_status()
    body = resp.json()
    challenge = body["challenge"]
    token = body["token"]
    return challenge, token, challenge["c"], challenge["s"], challenge["d"]


def _build_challenges(token: str, c_count: int, s_len: int, d_len: int) -> list[tuple[str, str]]:
    out = []
    for t in range(1, c_count + 1):
        salt = prng_string(f"{token}{t}", s_len)
        target = prng_string(f"{token}{t}d", d_len)
        out.append((salt, target))
    return out


def _solve_parallel(challenges: list[tuple[str, str]], workers: int) -> list[int]:
    c_count = len(challenges)
    solutions = [0] * c_count
    multiprocessing.freeze_support()
    executor = ProcessPoolExecutor(max_workers=workers)
    try:
        future_to_idx = {executor.submit(_solve_worker, chal): idx for idx, chal in enumerate(challenges)}
        solved = 0
        for fut in as_completed(future_to_idx):
            idx = future_to_idx[fut]
            solutions[idx] = fut.result()
            solved += 1
            if solved % 10 == 0 or solved == c_count:
                _logger.debug("Solved %d/%d", solved, c_count)
    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)
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
    return solutions


def _redeem_token(session: requests.Session, pow_url: str, token: str, solutions: list[int]) -> Optional[str]:
    _logger.debug("Redeeming captcha token...")
    resp = session.post(f"{pow_url}/api/redeem", json={"token": token, "solutions": solutions}, timeout=_TIMEOUT)
    resp.raise_for_status()
    redeem_data = resp.json()
    if not redeem_data.get("success"):
        _logger.warning("Python solver redeem rejected: %s", redeem_data)
        return None
    captcha_token = redeem_data["token"]
    _logger.info("Captcha token redeemed successfully.")
    return captcha_token


def _solve_python(pow_url: str, workers: int) -> Optional[str]:
    session = _captcha_session()
    _challenge, token, c_count, s_len, d_len = _fetch_challenge(session, pow_url)
    _logger.debug("Challenge: c=%d, s=%d, d=%d", c_count, s_len, d_len)
    challenges = _build_challenges(token, c_count, s_len, d_len)
    _logger.info("Solving %d captcha challenges with %d workers...", c_count, workers)
    t0 = time.monotonic()
    solutions = _solve_parallel(challenges, workers)
    _logger.debug("All challenges solved in %.1fs", time.monotonic() - t0)
    return _redeem_token(session, pow_url, token, solutions)


__all__ = ["_solve_python"]
