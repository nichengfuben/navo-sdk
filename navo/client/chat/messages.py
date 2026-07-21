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


class NavoMessagesMixin:
    # ======================================================================
    # 群组/频道管理
    # ======================================================================

    @require_login
    def create_channel(self, name: str, topic=None, is_private=None, icon=None, member_ids=None) -> Conversation:
        body: Dict[str, Any] = {"name": name}
        if topic is not None: body["topic"] = topic
        if is_private is not None: body["isPrivate"] = is_private
        if icon is not None: body["icon"] = icon
        if member_ids is not None: body["memberIds"] = member_ids
        data = self._http.request("POST", "/api/channels", json_data=body)
        return Conversation.from_dict(data)

    @async_require_login
    async def acreate_channel(self, name: str, topic=None, is_private=None, icon=None, member_ids=None) -> Conversation:
        body: Dict[str, Any] = {"name": name}
        if topic is not None: body["topic"] = topic
        if is_private is not None: body["isPrivate"] = is_private
        if icon is not None: body["icon"] = icon
        if member_ids is not None: body["memberIds"] = member_ids
        data = await self._http.arequest("POST", "/api/channels", json_data=body)
        return Conversation.from_dict(data)

    @require_login
    def update_channel(self, channel_id: str, name=None, topic=None, announcement=None,
                       icon=None, avatar_url=None, mute_all=None,
                       members_can_invite=None, is_private=None) -> Conversation:
        patch: Dict[str, Any] = {}
        if name is not None: patch["name"] = name
        if topic is not None: patch["topic"] = topic
        if announcement is not None: patch["announcement"] = announcement
        if icon is not None: patch["icon"] = icon
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if mute_all is not None: patch["muteAll"] = mute_all
        if members_can_invite is not None: patch["membersCanInvite"] = members_can_invite
        if is_private is not None: patch["isPrivate"] = is_private
        data = self._http.request("PATCH", f"/api/channels/{channel_id}", json_data=patch)
        return Conversation.from_dict(data)

    @async_require_login
    async def aupdate_channel(self, channel_id: str, name=None, topic=None, announcement=None,
                              icon=None, avatar_url=None, mute_all=None,
                              members_can_invite=None, is_private=None) -> Conversation:
        patch: Dict[str, Any] = {}
        if name is not None: patch["name"] = name
        if topic is not None: patch["topic"] = topic
        if announcement is not None: patch["announcement"] = announcement
        if icon is not None: patch["icon"] = icon
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if mute_all is not None: patch["muteAll"] = mute_all
        if members_can_invite is not None: patch["membersCanInvite"] = members_can_invite
        if is_private is not None: patch["isPrivate"] = is_private
        data = await self._http.arequest("PATCH", f"/api/channels/{channel_id}", json_data=patch)
        return Conversation.from_dict(data)

    @require_login
    def delete_channel(self, channel_id: str) -> bool:
        self._http.request("DELETE", f"/api/channels/{channel_id}")
        return True

    @async_require_login
    async def adelete_channel(self, channel_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/channels/{channel_id}")
        return True

    @require_login
    def leave_channel(self, channel_id: str) -> bool:
        self._http.request("POST", f"/api/channels/{channel_id}/leave")
        return True

    @async_require_login
    async def aleave_channel(self, channel_id: str) -> bool:
        await self._http.arequest("POST", f"/api/channels/{channel_id}/leave")
        return True

    @require_login
    def create_dm(self, user_id: str) -> Conversation:
        data = self._http.request("POST", "/api/dms", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @async_require_login
    async def acreate_dm(self, user_id: str) -> Conversation:
        data = await self._http.arequest("POST", "/api/dms", json_data={"userId": user_id})
        return Conversation.from_dict(data)

