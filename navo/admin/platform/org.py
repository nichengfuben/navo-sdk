from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminOrgMixin:
    # ======================================================================
    # Organizations & OSS
    # ======================================================================

    @require_login
    def list_organizations(self) -> List[Dict[str, Any]]:
        return self._http.request("GET", "/api/admin/organizations")

    @async_require_login
    async def alist_organizations(self) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", "/api/admin/organizations")

    @require_login
    def create_organization(self, name: str, parent_id: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/organizations", json_data=_body(
            name=name, parentId=parent_id, description=description,
        ))

    @async_require_login
    async def acreate_organization(self, name: str, parent_id: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/organizations", json_data=_body(
            name=name, parentId=parent_id, description=description,
        ))

    @require_login
    def delete_organization(self, org_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/organizations/{org_id}")

    @async_require_login
    async def adelete_organization(self, org_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/organizations/{org_id}")

    @require_login
    def list_organization_members(self, org_id: str) -> List[Dict[str, Any]]:
        return self._http.request("GET", f"/api/admin/organizations/{org_id}/members")

    @async_require_login
    async def alist_organization_members(self, org_id: str) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", f"/api/admin/organizations/{org_id}/members")

    @require_login
    def get_organization_path(self, org_id: str) -> List[Dict[str, Any]]:
        return self._http.request("GET", f"/api/admin/organizations/{org_id}/path")

    @async_require_login
    async def aget_organization_path(self, org_id: str) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", f"/api/admin/organizations/{org_id}/path")

    @require_login
    def list_oss_bindings(self) -> List[Dict[str, Any]]:
        return self._http.request("GET", "/api/admin/oss-bindings")

    @async_require_login
    async def alist_oss_bindings(self) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", "/api/admin/oss-bindings")

    @require_login
    def create_oss_binding(self, binding: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/oss-bindings", json_data=binding)

    @async_require_login
    async def acreate_oss_binding(self, binding: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/oss-bindings", json_data=binding)

    @require_login
    def delete_oss_binding(self, binding_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/oss-bindings/{binding_id}")

    @async_require_login
    async def adelete_oss_binding(self, binding_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/oss-bindings/{binding_id}")

    @require_login
    def set_default_oss_binding(self, binding_id: str) -> Dict[str, Any]:
        return self._http.request("PUT", f"/api/admin/oss-bindings/{binding_id}/default")

    @async_require_login
    async def aset_default_oss_binding(self, binding_id: str) -> Dict[str, Any]:
        return await self._http.arequest("PUT", f"/api/admin/oss-bindings/{binding_id}/default")

