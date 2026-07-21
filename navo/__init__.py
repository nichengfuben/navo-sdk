"""Navo IM SDK 统一导入层。"""

from __future__ import annotations

import sys
import threading
import types
from typing import Any, Callable, Dict, List, Optional

from navo.navo import Navo
from navo.admin import NavoAdmin
from navo.util import (
    SDKConfig,
    Container,
    require_login,
    async_require_login,
    auto_retry,
    validate_params,
    ChannelRole,
    ClientEventType,
    ConversationKind,
    FriendshipDirection,
    FriendshipStatus,
    Gender,
    MessageFormat,
    MessageKind,
    PresenceStatus,
    RegisterType,
    CallKind,
    CallTrackKind,
    SystemRole,
    ServerEventType,
    EnvManager,
    EventEmitter,
    AuthError,
    ConfigError,
    NavoError,
    NetworkError,
    TimeoutError,
    ValidationError,
    setup_logging,
    MessageBuilder,
    Attachment,
    BootstrapData,
    Conversation,
    ConversationMember,
    FriendRequest,
    Friendship,
    ForwardedMessage,
    Message,
    Notification,
    Organization,
    PollData,
    PollResult,
    Reaction,
    Sticker,
    StickerPack,
    User,
    TokenStore,
    FileUploader,
)

__version__ = "2.1.3"
__author__ = "navo-sdk"
__license__ = "MIT"


# ============================================================================
# 全局实例管理器
# ============================================================================


class _InstanceManager:
    """线程安全的全局 Navo 实例管理器。"""

    _DEFAULT = "__default__"

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._instances: Dict[str, Navo] = {}
        self._current: Optional[str] = None

    def init(self, username: str, password: str, name: Optional[str] = None, **kw: Any) -> Navo:
        """初始化全局默认实例并同步登录。"""
        return self._register(
            Navo(**kw).login(username, password), name,
        )

    async def ainit(self, username: str, password: str, name: Optional[str] = None, **kw: Any) -> Navo:
        """异步初始化全局默认实例并登录。"""
        im = Navo(**kw)
        await im.alogin(username, password)
        return self._register(im, name)

    def create(self, username: str, password: str, name: str = _DEFAULT, set_current: bool = True, **kw: Any) -> Navo:
        """创建并注册命名实例（同步登录）。"""
        im = Navo(**kw).login(username, password)
        return self._register(im, name, set_current)

    async def acreate(self, username: str, password: str, name: str = _DEFAULT, set_current: bool = True, **kw: Any) -> Navo:
        """异步创建并注册命名实例。"""
        im = Navo(**kw)
        await im.alogin(username, password)
        return self._register(im, name, set_current)

    def register(self, im: Navo, name: Optional[str] = None, set_current: bool = True) -> Navo:
        """注册已有 Navo 实例。"""
        return self._register(im, name, set_current)

    def _register(self, im: Navo, name: Optional[str] = None, set_current: bool = True) -> Navo:
        key = name or self._DEFAULT
        with self._lock:
            self._instances[key] = im
            if set_current or self._current is None:
                self._current = key
        return im

    def get_instance(self, name: Optional[str] = None) -> Navo:
        """获取指定名称的实例。"""
        with self._lock:
            key = name or self._current
            if key is None or key not in self._instances:
                raise NavoError("Navo 未初始化，请先调用 navo.init() 或 Navo().login()")
            return self._instances[key]

    get = get_instance

    def use(self, name: str) -> Navo:
        """切换当前活跃实例。"""
        with self._lock:
            if name not in self._instances:
                raise NavoError(f"实例 '{name}' 不存在，已注册: {list(self._instances.keys())}")
            self._current = name
            return self._instances[name]

    def list_instances(self) -> List[str]:
        """列出所有已注册的实例名称。"""
        with self._lock:
            return list(self._instances.keys())

    def has(self, name: str) -> bool:
        """检查指定名称的实例是否已注册。"""
        with self._lock:
            return name in self._instances

    @property
    def is_initialized(self) -> bool:
        with self._lock:
            return bool(self._instances)

    @property
    def current_name(self) -> Optional[str]:
        with self._lock:
            return self._current

    def remove(self, name: str) -> None:
        """移除并关闭指定实例（同步）。"""
        with self._lock:
            im = self._instances.pop(name, None)
            if self._current == name:
                keys = list(self._instances.keys())
                self._current = keys[0] if keys else None
        if im is not None:
            try:
                im.close()
            except Exception:
                pass

    async def aremove(self, name: str) -> None:
        """异步移除并关闭指定实例。"""
        with self._lock:
            im = self._instances.pop(name, None)
            if self._current == name:
                keys = list(self._instances.keys())
                self._current = keys[0] if keys else None
        if im is not None:
            try:
                await im.aclose()
            except Exception:
                pass

    def destroy(self) -> None:
        """销毁所有实例并重置管理器（同步）。"""
        with self._lock:
            instances = list(self._instances.values())
            self._instances.clear()
            self._current = None
        for im in instances:
            try:
                im.close()
            except Exception:
                pass

    async def adestroy(self) -> None:
        """异步销毁所有实例并重置管理器。"""
        with self._lock:
            instances = list(self._instances.values())
            self._instances.clear()
            self._current = None
        for im in instances:
            try:
                await im.aclose()
            except Exception:
                pass

    def reset(self) -> None:
        """重置管理器。"""
        self.destroy()


_mgr = _InstanceManager()


# ============================================================================
# 模块代理
# ============================================================================


class _NavoModule(types.ModuleType):
    """模块级代理。拦截属性访问，代理到当前活跃 Navo 实例。"""

    _MANAGER_METHODS = frozenset({
        "init", "ainit", "create", "acreate", "register",
        "get_instance", "get", "use", "list_instances", "has",
        "is_initialized", "current_name", "remove", "aremove",
        "destroy", "adestroy", "reset",
    })

    def __getattr__(self, name: str) -> Any:
        # 1. 管理器方法
        if name in self._MANAGER_METHODS:
            attr = getattr(_mgr, name, None)
            if attr is not None:
                return attr

        # 2. 事件注册
        if name in ("on_message", "on_event", "off_message"):
            return getattr(_mgr.get_instance(), name)

        # 3. 代理到当前活跃实例
        if _mgr.is_initialized:
            try:
                im = _mgr.get_instance()
                return getattr(im, name)
            except (NavoError, AttributeError):
                pass

        raise AttributeError(f"module 'navo' has no attribute '{name}'")

    def __dir__(self) -> List[str]:
        base = list(super().__dir__())
        base.extend(self._MANAGER_METHODS)
        if _mgr.is_initialized:
            try:
                im = _mgr.get_instance()
                base.extend(a for a in dir(im) if not a.startswith("_") and a not in base)
            except NavoError:
                pass
        return base


# ============================================================================
# 替换 sys.modules
# ============================================================================

_this_module = sys.modules[__name__]
_proxy_module = _NavoModule(__name__, __doc__)

for _attr_name in list(vars(_this_module).keys()):
    if not _attr_name.startswith("__") or _attr_name in (
        "__version__", "__author__", "__license__", "__all__",
        "__file__", "__spec__", "__path__", "__package__",
        "__loader__", "__builtins__",
    ):
        try:
            setattr(_proxy_module, _attr_name, getattr(_this_module, _attr_name))
        except (AttributeError, TypeError):
            pass

_proxy_module.__version__ = __version__
_proxy_module.__author__ = __author__
_proxy_module.__license__ = __license__
_proxy_module.__package__ = __package__

if hasattr(_this_module, "__path__"):
    _proxy_module.__path__ = _this_module.__path__
if hasattr(_this_module, "__file__"):
    _proxy_module.__file__ = _this_module.__file__
if hasattr(_this_module, "__spec__"):
    _proxy_module.__spec__ = _this_module.__spec__

sys.modules[__name__] = _proxy_module


# ============================================================================
# 便捷登录函数
# ============================================================================


def quick_login(username: str, password: str, **kw: Any) -> Navo:
    """同步便捷登录。"""
    return _mgr.init(username, password, **kw)


async def aquick_login(username: str, password: str, **kw: Any) -> Navo:
    """异步便捷登录。"""
    return await _mgr.ainit(username, password, **kw)


_proxy_module.quick_login = quick_login
_proxy_module.aquick_login = aquick_login


# ============================================================================
# __all__
# ============================================================================

__all__ = [
    # 核心类
    "Navo", "NavoAdmin", "quick_login", "aquick_login",
    # 全局管理
    "init", "ainit", "create", "acreate", "register",
    "get_instance", "get", "use",
    "list_instances", "has", "is_initialized", "current_name",
    "remove", "aremove", "destroy", "adestroy", "reset",
    # 枚举
    "ChannelRole", "ClientEventType", "ConversationKind",
    "FriendshipDirection", "FriendshipStatus", "Gender", "MessageFormat",
    "MessageKind", "PresenceStatus", "RegisterType", "CallKind", "CallTrackKind",
    "SystemRole", "ServerEventType",
    # 异常
    "NavoError", "AuthError", "NetworkError", "ValidationError",
    "TimeoutError", "ConfigError",
    # 数据模型
    "User", "Message", "Attachment", "Reaction",
    "BootstrapData", "Conversation", "ConversationMember",
    "Friendship", "FriendRequest", "ForwardedMessage", "Notification",
    "Organization", "PollData", "PollResult", "Sticker", "StickerPack",
    # 配置
    "SDKConfig", "EnvManager",
    # 协议
    "TokenStore",
    # 工具
    "Container", "EventEmitter", "MessageBuilder", "FileUploader",
    "setup_logging",
    # 装饰器
    "require_login", "async_require_login", "auto_retry", "validate_params",
]
