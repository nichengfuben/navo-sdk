from __future__ import annotations

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Optional, Tuple, Type

from navo.util.exceptions import AuthError, NavoError, ValidationError

_logger = logging.getLogger("navo")


def require_login(func: Callable[..., Any]) -> Callable[..., Any]:
    """同步登录状态检查装饰器。"""

    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        _check_login(self)
        return func(self, *args, **kwargs)

    return wrapper


def async_require_login(func: Callable[..., Any]) -> Callable[..., Any]:
    """异步登录状态检查装饰器。"""

    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        _check_login(self)
        return await func(self, *args, **kwargs)

    return wrapper


def _check_login(instance: Any) -> None:
    """检查实例是否已登录。"""
    token_store = getattr(instance, "_token_store", None)
    if token_store is None:
        raise AuthError("请先登录")
    token = token_store.get_token()
    if not token:
        raise AuthError("请先登录")


def auto_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """自动重试装饰器，支持指数退避。同步和异步方法均可装饰。"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                last_error: Optional[Exception] = None
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as exc:
                        last_error = exc
                        if attempt < max_retries - 1:
                            wait = delay * (2 ** attempt)
                            _logger.warning(
                                "重试 %s/%s，等待 %ss: %s", attempt + 1, max_retries, wait, exc,
                            )
                            await asyncio.sleep(wait)
                if last_error is not None:
                    raise last_error
                raise NavoError("重试失败")

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Optional[Exception] = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_error = exc
                    if attempt < max_retries - 1:
                        wait = delay * (2 ** attempt)
                        _logger.warning(
                            "重试 %s/%s，等待 %ss: %s", attempt + 1, max_retries, wait, exc,
                        )
                        time.sleep(wait)
            if last_error is not None:
                raise last_error
            raise NavoError("重试失败")

        return sync_wrapper

    return decorator


def validate_params(
    **validators: Callable[[Any], bool],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """参数验证装饰器。验证失败时抛出 ValidationError。"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for param_name, validator in validators.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not validator(value):
                        raise ValidationError(f"参数 '{param_name}' 验证失败: {value!r}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = [
    "require_login",
    "async_require_login",
    "auto_retry",
    "validate_params",
]
