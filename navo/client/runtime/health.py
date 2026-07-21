from __future__ import annotations

import asyncio
import logging

from typing import Any, Callable, Dict, List, Optional

from navo.util.config import SDKConfig, EnvManager
from navo.util.container import Container
from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Attachment, BootstrapData, Conversation, FriendRequest,
    Friendship, Message, User,
)
from navo.util.types.protocols import TokenStore
from navo.util.exceptions import AuthError, NavoError
from navo.util.transport import FileUploader, HTTPTransport, WebSocketTransport, setup_logging
from navo.captcha import solve_captcha_sync, asolve_captcha
from navo.admin import NavoAdmin

_logger = logging.getLogger("navo")


class NavoHealthMixin:
    # ======================================================================
    # 健康检查
    # ======================================================================

    def health(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/health")

    async def ahealth(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/health")


__all__ = ["Navo"]
