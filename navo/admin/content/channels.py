from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminChannelsMixin:
    # ======================================================================
    # Channels
    # ======================================================================

    @require_login
    def list_channels(self, page: Optional[int] = None, limit: Optional[int] = None, search: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/channels", params=_body(page=page, limit=limit, search=search))

    @async_require_login
    async def alist_channels(self, page: Optional[int] = None, limit: Optional[int] = None, search: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/channels", params=_body(page=page, limit=limit, search=search))

    @require_login
    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/admin/channels/{channel_id}")

    @async_require_login
    async def aget_channel(self, channel_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/admin/channels/{channel_id}")

    @require_login
    def delete_channel(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/channels/{channel_id}")

    @async_require_login
    async def adelete_channel(self, channel_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/channels/{channel_id}")

    @require_login
    def ban_channel(self, channel_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/channels/{channel_id}/ban", json_data=_body(reason=reason))

    @async_require_login
    async def aban_channel(self, channel_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/channels/{channel_id}/ban", json_data=_body(reason=reason))

    @require_login
    def unban_channel(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/channels/{channel_id}/unban")

    @async_require_login
    async def aunban_channel(self, channel_id: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/channels/{channel_id}/unban")

    @require_login
    def get_channel_ban_status(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/admin/channels/{channel_id}/ban-status")

    @async_require_login
    async def aget_channel_ban_status(self, channel_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/admin/channels/{channel_id}/ban-status")

    @require_login
    def add_channel_member(self, channel_id: str, user_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/channels/{channel_id}/members", json_data={"userId": user_id})

    @async_require_login
    async def aadd_channel_member(self, channel_id: str, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/channels/{channel_id}/members", json_data={"userId": user_id})

    @require_login
    def transfer_channel_owner(self, channel_id: str, user_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/channels/{channel_id}/transfer-owner", json_data={"userId": user_id})

    @async_require_login
    async def atransfer_channel_owner(self, channel_id: str, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/channels/{channel_id}/transfer-owner", json_data={"userId": user_id})

