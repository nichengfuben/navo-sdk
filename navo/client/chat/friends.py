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


class NavoFriendsMixin:
    # ======================================================================
    # 好友系统
    # ======================================================================

    @require_login
    def send_friend_request(self, username: str, message: str = "") -> Dict[str, Any]:
        return self._http.request("POST", "/api/friends/request", json_data={"username": username, "message": message})

    @async_require_login
    async def asend_friend_request(self, username: str, message: str = "") -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/friends/request", json_data={"username": username, "message": message})

    @require_login
    def accept_friend_request(self, request_id: str) -> bool:
        self._http.request("POST", f"/api/friends/requests/{request_id}/accept")
        return True

    @async_require_login
    async def aaccept_friend_request(self, request_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/requests/{request_id}/accept")
        return True

    @require_login
    def decline_friend_request(self, request_id: str) -> bool:
        self._http.request("POST", f"/api/friends/requests/{request_id}/decline")
        return True

    @async_require_login
    async def adecline_friend_request(self, request_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/requests/{request_id}/decline")
        return True

    @require_login
    def remove_friend(self, user_id: str) -> bool:
        self._http.request("DELETE", f"/api/friends/{user_id}")
        return True

    @async_require_login
    async def aremove_friend(self, user_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/friends/{user_id}")
        return True

    @require_login
    def block_user(self, user_id: str) -> bool:
        self._http.request("POST", f"/api/friends/{user_id}/block")
        return True

    @async_require_login
    async def ablock_user(self, user_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/{user_id}/block")
        return True

    @require_login
    def unblock_user(self, user_id: str) -> bool:
        self._http.request("POST", f"/api/friends/{user_id}/unblock")
        return True

    @async_require_login
    async def aunblock_user(self, user_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/{user_id}/unblock")
        return True

    @require_login
    def get_friendship(self, user_id: str) -> Friendship:
        data = self._http.request("GET", f"/api/friends/{user_id}")
        return Friendship.from_dict(data)

    @async_require_login
    async def aget_friendship(self, user_id: str) -> Friendship:
        data = await self._http.arequest("GET", f"/api/friends/{user_id}")
        return Friendship.from_dict(data)

