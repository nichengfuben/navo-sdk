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


class NavoProfileMixin:
    # ======================================================================
    # 用户
    # ======================================================================

    @require_login
    def get_me(self) -> User:
        data = self._http.request("GET", "/api/me")
        self._me = User.from_dict(data)
        return self._me

    @async_require_login
    async def aget_me(self) -> User:
        data = await self._http.arequest("GET", "/api/me")
        self._me = User.from_dict(data)
        return self._me

    @require_login
    def update_profile(self, display_name=None, bio=None, gender=None,
                       avatar_url=None, avatar_color=None, require_friend_approval=None,
                       language=None) -> User:
        patch: Dict[str, Any] = {}
        if display_name is not None: patch["displayName"] = display_name
        if bio is not None: patch["bio"] = bio
        if gender is not None: patch["gender"] = gender
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if avatar_color is not None: patch["avatarColor"] = avatar_color
        if require_friend_approval is not None: patch["requireFriendApproval"] = require_friend_approval
        if language is not None: patch["language"] = language
        data = self._http.request("PATCH", "/api/me", json_data=patch)
        self._me = User.from_dict(data)
        return self._me

    @async_require_login
    async def aupdate_profile(self, display_name=None, bio=None, gender=None,
                              avatar_url=None, avatar_color=None, require_friend_approval=None,
                              language=None) -> User:
        patch: Dict[str, Any] = {}
        if display_name is not None: patch["displayName"] = display_name
        if bio is not None: patch["bio"] = bio
        if gender is not None: patch["gender"] = gender
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if avatar_color is not None: patch["avatarColor"] = avatar_color
        if require_friend_approval is not None: patch["requireFriendApproval"] = require_friend_approval
        if language is not None: patch["language"] = language
        data = await self._http.arequest("PATCH", "/api/me", json_data=patch)
        self._me = User.from_dict(data)
        return self._me

    @require_login
    def change_password(
        self, current_password: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> bool:
        body: Dict[str, Any] = {
            "currentPassword": current_password, "newPassword": new_password,
        }
        if captcha_token is not None:
            body["captchaToken"] = captcha_token
        self._http.request("POST", "/api/me/password", json_data=body)
        return True

    @async_require_login
    async def achange_password(
        self, current_password: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> bool:
        body: Dict[str, Any] = {
            "currentPassword": current_password, "newPassword": new_password,
        }
        if captcha_token is not None:
            body["captchaToken"] = captcha_token
        await self._http.arequest("POST", "/api/me/password", json_data=body)
        return True

    @require_login
    def search_users(self, query: str) -> List[User]:
        data = self._http.request("GET", "/api/users/search", params={"q": query})
        return [User.from_dict(u) for u in data]

    @async_require_login
    async def asearch_users(self, query: str) -> List[User]:
        data = await self._http.arequest("GET", "/api/users/search", params={"q": query})
        return [User.from_dict(u) for u in data]

