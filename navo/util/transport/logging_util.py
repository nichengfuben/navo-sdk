from __future__ import annotations

import logging


def setup_logging(level=logging.INFO, fmt=None):
    logger = logging.getLogger("navo")
    root = logging.getLogger()
    if not logger.handlers:
        if not root.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(fmt or "%(asctime)s [%(levelname)s] %(name)s - %(message)s"))
            logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = True
    return logger


__all__ = ["setup_logging"]
