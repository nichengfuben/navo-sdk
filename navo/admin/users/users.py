from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminUsersMixin:
    # ======================================================================
    # Users
    # ======================================================================

    @require_login
    def list_users(self, page: Optional[int] = None, limit: Optional[int] = None, search: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/users", params=_body(page=page, limit=limit, search=search))

    @async_require_login
    async def alist_users(self, page: Optional[int] = None, limit: Optional[int] = None, search: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/users", params=_body(page=page, limit=limit, search=search))

    @require_login
    def get_user_role(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/admin/users/{user_id}/role")

    @async_require_login
    async def aget_user_role(self, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/admin/users/{user_id}/role")

    @require_login
    def grant_user_role(self, user_id: str, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/users/{user_id}/role", json_data=_body(
            role=kwargs.get("role"), permissions=kwargs.get("permissions"),
            note=kwargs.get("note"), expiresAt=kwargs.get("expires_at"),
        ))

    @async_require_login
    async def agrant_user_role(self, user_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/users/{user_id}/role", json_data=_body(
            role=kwargs.get("role"), permissions=kwargs.get("permissions"),
            note=kwargs.get("note"), expiresAt=kwargs.get("expires_at"),
        ))

    @require_login
    def revoke_user_role(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/users/{user_id}/role")

    @async_require_login
    async def arevoke_user_role(self, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/users/{user_id}/role")

    @require_login
    def ban_user(self, user_id: str, reason: Optional[str] = None, expires_at: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/users/{user_id}/ban", json_data=_body(
            reason=reason, expiresAt=expires_at,
        ))

    @async_require_login
    async def aban_user(self, user_id: str, reason: Optional[str] = None, expires_at: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/users/{user_id}/ban", json_data=_body(
            reason=reason, expiresAt=expires_at,
        ))

    @require_login
    def unban_user(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/users/{user_id}/unban")

    @async_require_login
    async def aunban_user(self, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/users/{user_id}/unban")

    @require_login
    def get_user_ban_status(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/admin/users/{user_id}/ban-status")

    @async_require_login
    async def aget_user_ban_status(self, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/admin/users/{user_id}/ban-status")

    @require_login
    def delete_user(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/users/{user_id}")

    @async_require_login
    async def adelete_user(self, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/users/{user_id}")

    @require_login
    def notify_user(self, user_id: str, content: str) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/users/{user_id}/notify", json_data={"content": content})

    @async_require_login
    async def anotify_user(self, user_id: str, content: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/users/{user_id}/notify", json_data={"content": content})

    @require_login
    def set_user_organization(self, user_id: str, org_id: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("PUT", f"/api/admin/users/{user_id}/organization", json_data=_body(orgId=org_id, title=title))

    @async_require_login
    async def aset_user_organization(self, user_id: str, org_id: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("PUT", f"/api/admin/users/{user_id}/organization", json_data=_body(orgId=org_id, title=title))

    @require_login
    def get_user_oss_bindings(self, user_id: str) -> List[Dict[str, Any]]:
        return self._http.request("GET", f"/api/admin/users/{user_id}/oss-bindings")

    @async_require_login
    async def aget_user_oss_bindings(self, user_id: str) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", f"/api/admin/users/{user_id}/oss-bindings")

