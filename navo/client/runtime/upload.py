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


class NavoUploadMixin:
    # ======================================================================
    # 文件上传
    # ======================================================================

    @require_login
    def upload_file(
        self, file_path: str, poster: Optional[str] = None,
        e2ee_conversation_id: Optional[str] = None,
    ) -> Attachment:
        return self._uploader.upload(file_path, poster=poster, e2ee_conversation_id=e2ee_conversation_id)

    @async_require_login
    async def aupload_file(
        self, file_path: str, poster: Optional[str] = None,
        e2ee_conversation_id: Optional[str] = None,
    ) -> Attachment:
        return await self._uploader.aupload(file_path, poster=poster, e2ee_conversation_id=e2ee_conversation_id)

