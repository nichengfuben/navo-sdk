from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminBaseMixin:

    # ======================================================================
    # Dashboard & identity
    # ======================================================================

    @require_login
    def dashboard(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/dashboard")

    @async_require_login
    async def adashboard(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/dashboard")

    @require_login
    def me(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/me")

    @async_require_login
    async def ame(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/me")

    def init(self, user_id: str, secret: str = "navo-admin-init-2024") -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/init", json_data={"userId": user_id, "secret": secret})

    async def ainit(self, user_id: str, secret: str = "navo-admin-init-2024") -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/init", json_data={"userId": user_id, "secret": secret})

