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


class NavoAuthMixin:
    # ======================================================================
    # 认证
    # ======================================================================

    def login(self, username: str, password: str) -> "Navo":
        captcha_token = solve_captcha_sync(self._config.pow_url)
        data = self._http.request("POST", "/api/auth/login", json_data={
            "username": username, "password": password,
            "captchaToken": captcha_token,
        })
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("登录成功: %s", username)
        return self

    async def alogin(self, username: str, password: str) -> "Navo":
        captcha_token = await asolve_captcha(self._config.pow_url)
        data = await self._http.arequest("POST", "/api/auth/login", json_data={
            "username": username, "password": password,
            "captchaToken": captcha_token,
        })
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("登录成功: %s", username)
        return self

    def register(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> "Navo":
        body: Dict[str, Any] = {
            "username": username, "password": password, "displayName": display_name,
        }
        for key, api_key in (
            ("type", "type"), ("email", "email"), ("phone", "phone"),
            ("code", "code"), ("captcha_token", "captchaToken"),
            ("invite_code", "inviteCode"),
        ):
            if kwargs.get(key) is not None:
                body[api_key] = kwargs[key]
        data = self._http.request("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("注册成功: %s", username)
        return self

    async def aregister(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> "Navo":
        body: Dict[str, Any] = {
            "username": username, "password": password, "displayName": display_name,
        }
        for key, api_key in (
            ("type", "type"), ("email", "email"), ("phone", "phone"),
            ("code", "code"), ("captcha_token", "captchaToken"),
            ("invite_code", "inviteCode"),
        ):
            if kwargs.get(key) is not None:
                body[api_key] = kwargs[key]
        data = await self._http.arequest("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("注册成功: %s", username)
        return self

