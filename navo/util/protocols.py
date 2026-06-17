from __future__ import annotations

from typing import Optional

try:
    from typing import Protocol, runtime_checkable
except ImportError:
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]


@runtime_checkable
class TokenStore(Protocol):
    """令牌存储协议。实现此协议可自定义令牌的持久化方式。"""

    def save_tokens(self, access_token: str, refresh_token: str) -> None:
        """保存访问令牌和刷新令牌。"""
        ...

    def get_access_token(self) -> Optional[str]:
        """获取访问令牌，不存在时返回 None。"""
        ...

    def get_refresh_token(self) -> Optional[str]:
        """获取刷新令牌，不存在时返回 None。"""
        ...

    def clear_tokens(self) -> None:
        """清除所有令牌。"""
        ...

    def save_token(self, token: str) -> None:
        """保存访问令牌（兼容旧接口）。"""
        ...

    def get_token(self) -> Optional[str]:
        """获取访问令牌（兼容旧接口）。"""
        ...

    def clear_token(self) -> None:
        """清除令牌（兼容旧接口）。"""
        ...


__all__ = ["TokenStore"]
