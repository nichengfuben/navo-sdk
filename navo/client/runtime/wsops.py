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


class NavoWsOpsMixin:
    # ======================================================================
    # WebSocket 消息发送
    # ======================================================================

    async def ws_auth(self, token: Optional[str] = None) -> None:
        t = token or self._token_store.get_token()
        if not t: raise AuthError("请先登录")
        await self._ws.start(t)

    async def ws_send_message(self, conversation_id: str, text: str = "", kind: Optional[str] = None,
                              attachments: Optional[List[Attachment]] = None, card_id: Optional[str] = None,
                              reply_to_id: Optional[str] = None, client_id: Optional[str] = None,
                              fmt: Optional[str] = None, source_conv_id: Optional[str] = None,
                              forward_message_ids: Optional[List[str]] = None,
                              captcha_token: Optional[str] = None, sticker_id: Optional[str] = None,
                              scheduled_at: Optional[str] = None, e2ee: Optional[bool] = None,
                              e2ee_session_id: Optional[str] = None) -> None:
        payload: Dict[str, Any] = {"conversationId": conversation_id, "text": text}
        if kind: payload["kind"] = kind
        if fmt: payload["format"] = fmt
        if attachments: payload["attachments"] = [a.to_dict() for a in attachments]
        if card_id: payload["cardId"] = card_id
        if reply_to_id: payload["replyToId"] = reply_to_id
        if source_conv_id: payload["sourceConvId"] = source_conv_id
        if forward_message_ids: payload["forwardMessageIds"] = forward_message_ids
        if captcha_token: payload["captchaToken"] = captcha_token
        if sticker_id: payload["stickerId"] = sticker_id
        if scheduled_at: payload["scheduledAt"] = scheduled_at
        if e2ee is not None: payload["e2ee"] = e2ee
        if e2ee_session_id: payload["e2eeSessionId"] = e2ee_session_id
        event: Dict[str, Any] = {"type": "message:send", "payload": payload}
        if client_id: event["clientId"] = client_id
        await self._ws.send(event)

    async def ws_recall_message(self, message_id: str) -> None:
        await self._ws.send({"type": "message:recall", "messageId": message_id})

    async def ws_edit_message(self, message_id: str, text: str) -> None:
        await self._ws.send({"type": "message:edit", "messageId": message_id, "text": text})

    async def ws_typing_start(self, conversation_id: str) -> None:
        await self._ws.send({"type": "typing:start", "conversationId": conversation_id})

    async def ws_typing_stop(self, conversation_id: str) -> None:
        await self._ws.send({"type": "typing:stop", "conversationId": conversation_id})

    async def ws_set_presence(self, status: str) -> None:
        await self._ws.send({"type": "presence:set", "status": status})

    async def ws_toggle_reaction(self, message_id: str, emoji: str) -> None:
        await self._ws.send({"type": "reaction:toggle", "messageId": message_id, "emoji": emoji})

    async def ws_mark_read(self, conversation_id: str, message_id: str) -> None:
        await self._ws.send({"type": "read", "conversationId": conversation_id, "messageId": message_id})

