from __future__ import annotations

import logging
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    fmt: Optional[str] = None,
) -> logging.Logger:
    """配置 SDK 日志。

    Args:
        level: 日志级别
        fmt: 日志格式字符串

    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger("navo")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(fmt or "%(asctime)s [%(levelname)s] %(name)s - %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


__all__ = ["setup_logging"]
