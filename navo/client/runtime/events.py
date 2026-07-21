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


class NavoEventsMixin:
    # ======================================================================
    # 事件注册
    # ======================================================================

    def on_message(self, handler):
        self._ws.on("message:new", handler)
        return self

    def off_message(self, handler):
        self._ws.off("message:new", handler)
        return self

    def on_event(self, event_type, handler):
        self._ws.on(event_type, handler)
        return self

    async def listen(self):
        while self._ws._running:
            await asyncio.sleep(1)

    def listen_sync(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running(): raise NavoError("事件循环已在运行")
        except RuntimeError: pass
        loop = asyncio.new_event_loop()
        try: loop.run_until_complete(self.listen())
        except KeyboardInterrupt: pass
        finally: loop.close()

    async def start_listening(self): asyncio.create_task(self.listen())
    async def stop_listening(self): await self._ws.stop()

