from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtNotifyMixin:
    # ======================================================================
    # 通知 / 举报 / 翻译 / 组织 / 贴纸 / 推送 / NSFW
    # ======================================================================

    @require_login
    def get_notifications(self) -> List[Notification]:
        data = self._http.request("GET", "/api/notifications")
        return [Notification.from_dict(n) for n in data]

    @async_require_login
    async def aget_notifications(self) -> List[Notification]:
        data = await self._http.arequest("GET", "/api/notifications")
        return [Notification.from_dict(n) for n in data]

    @require_login
    def mark_notification_read(self, notification_id: str) -> bool:
        self._http.request("POST", f"/api/notifications/{notification_id}/read")
        return True

    @async_require_login
    async def amark_notification_read(self, notification_id: str) -> bool:
        await self._http.arequest("POST", f"/api/notifications/{notification_id}/read")
        return True

    @require_login
    def create_report(
        self, target_type: str, target_id: str, reason: str,
        screenshot_url: Optional[str] = None, captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._http.request("POST", "/api/reports", json_data=_body(
            targetType=target_type, targetId=target_id, reason=reason,
            screenshotUrl=screenshot_url, captchaToken=captcha_token,
        ))

    @async_require_login
    async def acreate_report(
        self, target_type: str, target_id: str, reason: str,
        screenshot_url: Optional[str] = None, captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/reports", json_data=_body(
            targetType=target_type, targetId=target_id, reason=reason,
            screenshotUrl=screenshot_url, captchaToken=captcha_token,
        ))

    @require_login
    def translate(self, text: str, target_lang: str) -> str:
        data = self._http.request("POST", "/api/translate", json_data={
            "text": text, "targetLang": target_lang,
        })
        return data.get("result", "")

    @async_require_login
    async def atranslate(self, text: str, target_lang: str) -> str:
        data = await self._http.arequest("POST", "/api/translate", json_data={
            "text": text, "targetLang": target_lang,
        })
        return data.get("result", "")

    @require_login
    def get_organization(self, org_id: str) -> Dict[str, Any]:
        data = self._http.request("GET", f"/api/orgs/{org_id}")
        return {
            "org": Organization.from_dict(data.get("org", {})),
            "path": [Organization.from_dict(o) for o in data.get("path", [])],
        }

    @async_require_login
    async def aget_organization(self, org_id: str) -> Dict[str, Any]:
        data = await self._http.arequest("GET", f"/api/orgs/{org_id}")
        return {
            "org": Organization.from_dict(data.get("org", {})),
            "path": [Organization.from_dict(o) for o in data.get("path", [])],
        }

    @require_login
    def get_sticker_packs(self) -> List[StickerPack]:
        data = self._http.request("GET", "/api/sticker-packs")
        return [StickerPack.from_dict(p) for p in data]

    @async_require_login
    async def aget_sticker_packs(self) -> List[StickerPack]:
        data = await self._http.arequest("GET", "/api/sticker-packs")
        return [StickerPack.from_dict(p) for p in data]

    @require_login
    def register_push_token(self, token: str) -> bool:
        self._http.request("POST", "/api/push/register", json_data={"token": token})
        return True

    @async_require_login
    async def aregister_push_token(self, token: str) -> bool:
        await self._http.arequest("POST", "/api/push/register", json_data={"token": token})
        return True

    @require_login
    def unregister_push_token(self, token: Optional[str] = None) -> bool:
        body = _body(token=token)
        self._http.request("POST", "/api/push/unregister", json_data=body or {})
        return True

    @async_require_login
    async def aunregister_push_token(self, token: Optional[str] = None) -> bool:
        body = _body(token=token)
        await self._http.arequest("POST", "/api/push/unregister", json_data=body or {})
        return True

    @require_login
    def check_nsfw(self, file_path: str) -> Dict[str, Any]:
        return self._uploader.check_nsfw(file_path)

    @async_require_login
    async def acheck_nsfw(self, file_path: str) -> Dict[str, Any]:
        return await self._uploader.acheck_nsfw(file_path)

