from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtAccountMixin:
    # ======================================================================
    # 账户 / 资料扩展
    # ======================================================================

    @require_login
    def delete_account(self, password: str, captcha_token: Optional[str] = None) -> bool:
        self._http.request("DELETE", "/api/me", json_data=_body(
            password=password, captchaToken=captcha_token,
        ))
        self.logout()
        return True

    @async_require_login
    async def adelete_account(self, password: str, captcha_token: Optional[str] = None) -> bool:
        await self._http.arequest("DELETE", "/api/me", json_data=_body(
            password=password, captchaToken=captcha_token,
        ))
        await self.alogout()
        return True

    @require_login
    def bind_email(self, email: str, code: str) -> User:
        data = self._http.request("POST", "/api/me/email/bind", json_data={"email": email, "code": code})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @async_require_login
    async def abind_email(self, email: str, code: str) -> User:
        data = await self._http.arequest("POST", "/api/me/email/bind", json_data={"email": email, "code": code})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @require_login
    def change_email(self, new_email: str, code: str, password: str) -> User:
        data = self._http.request("POST", "/api/me/email/change", json_data={
            "newEmail": new_email, "code": code, "password": password,
        })
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @async_require_login
    async def achange_email(self, new_email: str, code: str, password: str) -> User:
        data = await self._http.arequest("POST", "/api/me/email/change", json_data={
            "newEmail": new_email, "code": code, "password": password,
        })
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @require_login
    def unbind_email(self, password: str) -> User:
        data = self._http.request("DELETE", "/api/me/email", json_data={"password": password})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @async_require_login
    async def aunbind_email(self, password: str) -> User:
        data = await self._http.arequest("DELETE", "/api/me/email", json_data={"password": password})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @require_login
    def bind_phone(self, phone: str, code: str) -> User:
        data = self._http.request("POST", "/api/me/phone/bind", json_data={"phone": phone, "code": code})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @async_require_login
    async def abind_phone(self, phone: str, code: str) -> User:
        data = await self._http.arequest("POST", "/api/me/phone/bind", json_data={"phone": phone, "code": code})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @require_login
    def change_phone(self, new_phone: str, code: str, password: str) -> User:
        data = self._http.request("POST", "/api/me/phone/change", json_data={
            "newPhone": new_phone, "code": code, "password": password,
        })
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @async_require_login
    async def achange_phone(self, new_phone: str, code: str, password: str) -> User:
        data = await self._http.arequest("POST", "/api/me/phone/change", json_data={
            "newPhone": new_phone, "code": code, "password": password,
        })
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @require_login
    def unbind_phone(self, password: str) -> User:
        data = self._http.request("DELETE", "/api/me/phone", json_data={"password": password})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @async_require_login
    async def aunbind_phone(self, password: str) -> User:
        data = await self._http.arequest("DELETE", "/api/me/phone", json_data={"password": password})
        self._me = User.from_dict(data.get("user", data))
        return self._me

    @require_login
    def get_second_password_status(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/me/second-password")

    @async_require_login
    async def aget_second_password_status(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/me/second-password")

    @require_login
    def set_second_password(self, password: str, hint: str, captcha_token: Optional[str] = None) -> bool:
        self._http.request("POST", "/api/me/second-password", json_data=_body(
            password=password, hint=hint, captchaToken=captcha_token,
        ))
        return True

    @async_require_login
    async def aset_second_password(self, password: str, hint: str, captcha_token: Optional[str] = None) -> bool:
        await self._http.arequest("POST", "/api/me/second-password", json_data=_body(
            password=password, hint=hint, captchaToken=captcha_token,
        ))
        return True

    @require_login
    def delete_second_password(self, captcha_token: Optional[str] = None) -> bool:
        self._http.request("DELETE", "/api/me/second-password", json_data=_body(captchaToken=captcha_token))
        return True

    @async_require_login
    async def adelete_second_password(self, captcha_token: Optional[str] = None) -> bool:
        await self._http.arequest("DELETE", "/api/me/second-password", json_data=_body(captchaToken=captcha_token))
        return True

