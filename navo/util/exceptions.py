from __future__ import annotations

from typing import Optional


class NavoError(Exception):
    """SDK 根异常。所有 Navo SDK 异常的公共基类，携带可选业务错误码。"""

    def __init__(self, message: str, code: Optional[int] = None) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __repr__(self) -> str:
        if self.code is not None:
            return f"{self.__class__.__name__}(code={self.code}, message={self.message!r})"
        return f"{self.__class__.__name__}(message={self.message!r})"


class AuthError(NavoError):
    """认证异常：未登录或令牌失效。"""


class NetworkError(NavoError):
    """网络异常：请求失败或连接中断。"""


class ValidationError(NavoError):
    """参数验证异常：入参不满足要求。"""


class TimeoutError(NavoError):
    """超时异常。"""


class ConfigError(NavoError):
    """配置异常：依赖未注册或配置错误。"""


__all__ = [
    "NavoError",
    "AuthError",
    "NetworkError",
    "ValidationError",
    "TimeoutError",
    "ConfigError",
]
