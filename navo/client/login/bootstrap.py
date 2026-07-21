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


class NavoBootstrapMixin:
    # ======================================================================
    # Bootstrap
    # ======================================================================

    @require_login
    def bootstrap(self) -> BootstrapData:
        data = self._http.request("GET", "/api/bootstrap")
        self._bootstrap = BootstrapData.from_dict(data)
        return self._bootstrap

    @async_require_login
    async def abootstrap(self) -> BootstrapData:
        data = await self._http.arequest("GET", "/api/bootstrap")
        self._bootstrap = BootstrapData.from_dict(data)
        return self._bootstrap

