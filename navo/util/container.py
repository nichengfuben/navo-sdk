from __future__ import annotations

from typing import Any, Callable, Dict

from navo.util.exceptions import ConfigError


class Container:
    """简单依赖注入容器。支持单例注册和工厂注册两种模式。"""

    def __init__(self) -> None:
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[["Container"], Any]] = {}
        self._instances: Dict[str, Any] = {}

    def register_singleton(self, name: str, instance: Any) -> "Container":
        """注册单例对象。"""
        self._singletons[name] = instance
        return self

    def register_factory(
        self, name: str, factory: Callable[["Container"], Any]
    ) -> "Container":
        """注册工厂函数（首次解析时创建并缓存实例）。"""
        self._factories[name] = factory
        return self

    def resolve(self, name: str) -> Any:
        """解析已注册的依赖。"""
        if name in self._singletons:
            return self._singletons[name]
        if name in self._instances:
            return self._instances[name]
        if name in self._factories:
            instance = self._factories[name](self)
            self._instances[name] = instance
            return instance
        raise ConfigError(f"未注册的依赖: {name}")

    def has(self, name: str) -> bool:
        """检查指定名称是否已注册。"""
        return (
            name in self._singletons
            or name in self._factories
            or name in self._instances
        )

    def reset(self) -> None:
        """重置所有由工厂创建的实例缓存（单例不受影响）。"""
        self._instances.clear()


__all__ = ["Container"]
