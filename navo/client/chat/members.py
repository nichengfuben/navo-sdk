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


class NavoMembersMixin:
    # ======================================================================
    # 群组成员管理
    # ======================================================================

    @require_login
    def add_member(self, channel_id: str, user_id: str) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/members", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @async_require_login
    async def aadd_member(self, channel_id: str, user_id: str) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/members", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @require_login
    def remove_member(self, channel_id: str, user_id: str) -> Conversation:
        data = self._http.request("DELETE", f"/api/channels/{channel_id}/members/{user_id}")
        return Conversation.from_dict(data)

    @async_require_login
    async def aremove_member(self, channel_id: str, user_id: str) -> Conversation:
        data = await self._http.arequest("DELETE", f"/api/channels/{channel_id}/members/{user_id}")
        return Conversation.from_dict(data)

    @require_login
    def set_role(self, channel_id: str, user_id: str, role: str) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/role", json_data={"userId": user_id, "role": role})
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_role(self, channel_id: str, user_id: str, role: str) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/role", json_data={"userId": user_id, "role": role})
        return Conversation.from_dict(data)

    @require_login
    def set_muted(self, channel_id: str, user_id: str, muted: bool) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/mute", json_data={"userId": user_id, "muted": muted})
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_muted(self, channel_id: str, user_id: str, muted: bool) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/mute", json_data={"userId": user_id, "muted": muted})
        return Conversation.from_dict(data)

    @require_login
    def set_banned(self, channel_id: str, user_id: str, banned: bool) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/ban", json_data={"userId": user_id, "banned": banned})
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_banned(self, channel_id: str, user_id: str, banned: bool) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/ban", json_data={"userId": user_id, "banned": banned})
        return Conversation.from_dict(data)

