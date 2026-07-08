from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

try:
    from dotenv import load_dotenv, set_key as dotenv_set_key
except ImportError:
    def load_dotenv(*args, **kwargs): pass
    def dotenv_set_key(*args, **kwargs): pass

import logging

_logger = logging.getLogger("navo")


class EnvManager:
    """环境变量管理器。"""

    def __init__(self, env_file: str = ".env") -> None:
        self._env_file = env_file
        self._cache: dict[str, str] = {}
        self._ensure_env_file()
        load_dotenv(self._env_file, override=True)

    def _ensure_env_file(self):
        if not os.path.exists(self._env_file):
            Path(self._env_file).write_text("# Navo SDK Configuration\n", encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache: return self._cache[key]
        value = os.environ.get(key)
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        str_value = str(value) if value is not None else ""
        self._cache[key] = str_value
        os.environ[key] = str_value
        try: dotenv_set_key(self._env_file, key, str_value)
        except Exception as exc: _logger.warning("写入环境变量文件失败: %s", exc)

    def get_int(self, key: str, default: int = 0) -> int:
        value = self.get(key, str(default))
        try: return int(value) if value else default
        except (ValueError, TypeError): return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get(key, str(default).lower())
        return str(value).lower() in ("true", "1", "yes", "on")

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)
        os.environ.pop(key, None)

    def save_token(self, token: str) -> None:
        self.set("NAVO_TOKEN", token)

    def get_token(self) -> Optional[str]:
        value = self.get("NAVO_TOKEN")
        return str(value) if value else None

    def clear_token(self) -> None:
        self.delete("NAVO_TOKEN")


__all__ = ["EnvManager"]
