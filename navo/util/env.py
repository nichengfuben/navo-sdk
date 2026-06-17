from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

try:
    from dotenv import load_dotenv, set_key as dotenv_set_key
except ImportError:
    def load_dotenv(*args: object, **kwargs: object) -> None:
        """dotenv 不可用时的空实现。"""

    def dotenv_set_key(*args: object, **kwargs: object) -> None:
        """dotenv 不可用时的空实现。"""

import logging

_logger = logging.getLogger("navo")


class EnvManager:
    """环境变量管理器。内存缓存 + .env 文件持久化。"""

    def __init__(self, env_file: str = ".env") -> None:
        self._env_file = env_file
        self._cache: dict[str, str] = {}
        self._ensure_env_file()
        load_dotenv(self._env_file, override=True)

    def _ensure_env_file(self) -> None:
        if not os.path.exists(self._env_file):
            Path(self._env_file).write_text("# Navo SDK Configuration\n", encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            return self._cache[key]
        value = os.environ.get(key)
        if value is not None:
            return value
        return default

    def set(self, key: str, value: Any) -> None:
        str_value = str(value) if value is not None else ""
        self._cache[key] = str_value
        os.environ[key] = str_value
        try:
            dotenv_set_key(self._env_file, key, str_value)
        except Exception as exc:
            _logger.warning("写入环境变量文件失败: %s", exc)

    def get_int(self, key: str, default: int = 0) -> int:
        value = self.get(key, str(default))
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get(key, str(default).lower())
        return str(value).lower() in ("true", "1", "yes", "on")

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)
        os.environ.pop(key, None)

    # TokenStore 协议实现

    def save_tokens(self, access_token: str, refresh_token: str) -> None:
        """保存访问令牌和刷新令牌。"""
        self.set("NAVO_ACCESS_TOKEN", access_token)
        self.set("NAVO_REFRESH_TOKEN", refresh_token)

    def get_access_token(self) -> Optional[str]:
        """获取访问令牌。"""
        value = self.get("NAVO_ACCESS_TOKEN")
        # Fallback to legacy NAVO_TOKEN
        if not value:
            value = self.get("NAVO_TOKEN")
        return str(value) if value else None

    def get_refresh_token(self) -> Optional[str]:
        """获取刷新令牌。"""
        value = self.get("NAVO_REFRESH_TOKEN")
        return str(value) if value else None

    def clear_tokens(self) -> None:
        """清除所有令牌。"""
        self.delete("NAVO_ACCESS_TOKEN")
        self.delete("NAVO_REFRESH_TOKEN")
        self.delete("NAVO_TOKEN")  # clear legacy token too

    def save_token(self, token: str) -> None:
        """保存访问令牌（兼容旧接口）。"""
        self.set("NAVO_ACCESS_TOKEN", token)

    def get_token(self) -> Optional[str]:
        """获取访问令牌（兼容旧接口）。"""
        return self.get_access_token()

    def clear_token(self) -> None:
        """清除令牌（兼容旧接口）。"""
        self.clear_tokens()


__all__ = ["EnvManager"]
