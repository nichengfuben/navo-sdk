from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtSystemMixin:
    # ======================================================================
    # 系统
    # ======================================================================

    def get_system_settings(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/system/settings")

    async def aget_system_settings(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/system/settings")

    def get_captcha_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/system/captcha-config")

    async def aget_captcha_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/system/captcha-config")

    def get_cdn_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/system/cdn-config")

    async def aget_cdn_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/system/cdn-config")

    def get_ice_servers(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/system/ice-servers")

    async def aget_ice_servers(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/system/ice-servers")

