from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

try:
    from dotenv import load_dotenv, set_key as dotenv_set_key
except ImportError:
    def load_dotenv(*args: object, **kwargs: object) -> None:
        """dotenv 不可用时的空实现。"""

    def dotenv_set_key(*args: object, **kwargs: object) -> None:
        """dotenv 不可用时的空实现。"""

_logger = logging.getLogger("navo")


@dataclass
class SDKConfig:
    """SDK 全局配置类。所有配置项均有合理默认值。"""

    base_url: str = "https://navo.airoe.cn"
    ws_url: str = "wss://navo.airoe.cn/ws"
    pow_url: str = "https://pow.airoe.cn"

    timeout: int = 30
    max_retries: int = 3
    retry_backoff_factor: float = 0.3
    retry_status_forcelist: List[int] = field(
        default_factory=lambda: [429, 500, 502, 503, 504]
    )

    max_upload_bytes: int = 25 * 1024 * 1024

    ws_reconnect_delay: int = 1
    ws_max_reconnect_delay: int = 300
    ws_heartbeat_interval: int = 20
    ws_ping_interval: int = 20
    ws_ping_timeout: int = 10
    ws_auth_timeout: float = 10.0
    ws_auto_reconnect: bool = True

    auto_refresh_token: bool = True
    token_refresh_margin: int = 60

    log_level: int = logging.INFO
    log_format: str = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    debug: bool = False
    ssl_verify: bool = False

    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 NavoSDK/1.0.0"
    )

    def __post_init__(self) -> None:
        if self.debug:
            self.log_level = logging.DEBUG

    @classmethod
    def from_env(cls, env_file: str = ".env") -> "SDKConfig":
        """从环境变量构造配置对象。"""
        if os.path.exists(env_file):
            load_dotenv(env_file, override=True)
        return cls(
            base_url=os.getenv("NAVO_BASE_URL", cls.base_url),
            ws_url=os.getenv("NAVO_WS_URL", cls.ws_url),
            pow_url=os.getenv("NAVO_POW_URL", cls.pow_url),
            timeout=int(os.getenv("NAVO_TIMEOUT", str(cls.timeout))),
            max_retries=int(os.getenv("NAVO_MAX_RETRIES", str(cls.max_retries))),
            debug=os.getenv("NAVO_DEBUG", "false").lower() in ("true", "1", "yes"),
            ssl_verify=os.getenv("NAVO_SSL_VERIFY", "false").lower() in ("true", "1", "yes"),
            auto_refresh_token=os.getenv("NAVO_AUTO_REFRESH_TOKEN", "true").lower()
            in ("true", "1", "yes"),
        )


class EnvManager:
    """环境变量与令牌持久化管理。"""

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
        return value if value is not None else default

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

    def save_token(self, token: str) -> None:
        self.set("NAVO_TOKEN", token)

    def get_token(self) -> Optional[str]:
        value = self.get("NAVO_TOKEN")
        return str(value) if value else None

    def clear_token(self) -> None:
        self.delete("NAVO_TOKEN")


__all__ = ["SDKConfig", "EnvManager"]
