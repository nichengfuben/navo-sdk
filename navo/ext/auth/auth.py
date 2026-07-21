from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtAuthMixin:
    # ======================================================================
    # 认证扩展
    # ======================================================================

    def send_verification_code(
        self, target: str, type_: str, purpose: str = "register",
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(target=target, type=type_, purpose=purpose, captchaToken=captcha_token)
        return self._http.request("POST", "/api/auth/verification-code", json_data=body)

    async def asend_verification_code(
        self, target: str, type_: str, purpose: str = "register",
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(target=target, type=type_, purpose=purpose, captchaToken=captcha_token)
        return await self._http.arequest("POST", "/api/auth/verification-code", json_data=body)

    def reset_password(
        self, target: str, type_: str, code: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(
            target=target, type=type_, code=code,
            newPassword=new_password, captchaToken=captcha_token,
        )
        return self._http.request("POST", "/api/auth/reset-password", json_data=body)

    async def areset_password(
        self, target: str, type_: str, code: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(
            target=target, type=type_, code=code,
            newPassword=new_password, captchaToken=captcha_token,
        )
        return await self._http.arequest("POST", "/api/auth/reset-password", json_data=body)

    def verify_second_password(self, token: str, password: str) -> User:
        data = self._http.request("POST", "/api/auth/verify-second-password", json_data={
            "token": token, "password": password,
        })
        return User.from_dict(data.get("user", data))

    async def averify_second_password(self, token: str, password: str) -> User:
        data = await self._http.arequest("POST", "/api/auth/verify-second-password", json_data={
            "token": token, "password": password,
        })
        return User.from_dict(data.get("user", data))

    def sso_initiate(self) -> Dict[str, Any]:
        return self._http.request("POST", "/api/auth/sso/initiate")

    async def asso_initiate(self) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/auth/sso/initiate")

    def sso_login(self) -> Dict[str, Any]:
        return self._http.request("POST", "/api/auth/sso")

    async def asso_login(self) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/auth/sso")

    def register_extended(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> Dict[str, Any]:
        body = _body(
            username=username, password=password, displayName=display_name,
            type=kwargs.get("type"), email=kwargs.get("email"),
            phone=kwargs.get("phone"), code=kwargs.get("code"),
            captchaToken=kwargs.get("captcha_token"),
            inviteCode=kwargs.get("invite_code"),
        )
        data = self._http.request("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        return data

    async def aregister_extended(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> Dict[str, Any]:
        body = _body(
            username=username, password=password, displayName=display_name,
            type=kwargs.get("type"), email=kwargs.get("email"),
            phone=kwargs.get("phone"), code=kwargs.get("code"),
            captchaToken=kwargs.get("captcha_token"),
            inviteCode=kwargs.get("invite_code"),
        )
        data = await self._http.arequest("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        return data

    def logout(self) -> None:
        self._token_store.clear_token()
        self._me = None

    async def alogout(self) -> None:
        self.logout()

