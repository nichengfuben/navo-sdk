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


class NavoConversationsMixin:
    # ======================================================================
    # 会话
    # ======================================================================

    @require_login
    def get_conversations(self) -> List[Conversation]:
        data = self._http.request("GET", "/api/conversations")
        return [Conversation.from_dict(c) for c in data]

    @async_require_login
    async def aget_conversations(self) -> List[Conversation]:
        data = await self._http.arequest("GET", "/api/conversations")
        return [Conversation.from_dict(c) for c in data]

    @require_login
    def get_messages(self, conversation_id: str, limit: int = 200, **kwargs) -> List[Message]:
        params: Dict[str, Any] = {}
        if "before" in kwargs: params["before"] = kwargs["before"]
        if "since" in kwargs: params["since"] = kwargs["since"]
        if "cursor" in kwargs: params["cursor"] = kwargs["cursor"]
        if "page" in kwargs: params["page"] = kwargs["page"]
        if "page_size" in kwargs: params["pageSize"] = kwargs["page_size"]
        if not params:
            params["pageSize"] = limit
        data = self._http.request("GET", f"/api/conversations/{conversation_id}/messages", params=params)
        if isinstance(data, list):
            return [Message.from_dict(m) for m in data]
        return [Message.from_dict(m) for m in data.get("items", [])]

    @async_require_login
    async def aget_messages(self, conversation_id: str, limit: int = 200, **kwargs) -> List[Message]:
        params: Dict[str, Any] = {}
        if "before" in kwargs: params["before"] = kwargs["before"]
        if "since" in kwargs: params["since"] = kwargs["since"]
        if "cursor" in kwargs: params["cursor"] = kwargs["cursor"]
        if "page" in kwargs: params["page"] = kwargs["page"]
        if "page_size" in kwargs: params["pageSize"] = kwargs["page_size"]
        if not params:
            params["pageSize"] = limit
        data = await self._http.arequest("GET", f"/api/conversations/{conversation_id}/messages", params=params)
        if isinstance(data, list):
            return [Message.from_dict(m) for m in data]
        return [Message.from_dict(m) for m in data.get("items", [])]

    @require_login
    def clear_history(self, conversation_id: str) -> bool:
        self._http.request("DELETE", f"/api/conversations/{conversation_id}/messages")
        return True

    @async_require_login
    async def aclear_history(self, conversation_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/conversations/{conversation_id}/messages")
        return True

