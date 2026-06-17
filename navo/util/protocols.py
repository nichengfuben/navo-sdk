from __future__ import annotations

from typing import Optional

try:
    from typing import Protocol, runtime_checkable
except ImportError:
    from typing_extensions import Protocol, runtime_checkable

@runtime_checkable
class TokenStore(Protocol):
    """令牌存储协议。"""

    def save_token(self, token: str) -> None:
        """保存访问令牌。"""
        ...

    def get_token(self) -> Optional[str]:
        """获取访问令牌。"""
        ...

    def clear_token(self) -> None:
        """清除令牌。"""
        ...


__all__ = ["TokenStore"]
