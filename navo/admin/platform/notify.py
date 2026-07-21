from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminNotifyMixin:
    # ======================================================================
    # Notifications (admin)
    # ======================================================================

    @require_login
    def list_notifications(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/notifications", params=_body(page=page, limit=limit))

    @async_require_login
    async def alist_notifications(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/notifications", params=_body(page=page, limit=limit))

    @require_login
    def list_private_notifications(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/notifications/private", params=_body(page=page, limit=limit))

    @async_require_login
    async def alist_private_notifications(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/notifications/private", params=_body(page=page, limit=limit))

    @require_login
    def create_notification(self, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/notifications", json_data=_body(
            title=kwargs.get("title"), content=kwargs.get("content"),
            imageUrl=kwargs.get("image_url"), targetUserId=kwargs.get("target_user_id"),
        ))

    @async_require_login
    async def acreate_notification(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/notifications", json_data=_body(
            title=kwargs.get("title"), content=kwargs.get("content"),
            imageUrl=kwargs.get("image_url"), targetUserId=kwargs.get("target_user_id"),
        ))

    @require_login
    def update_notification(self, notification_id: str, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("PUT", f"/api/admin/notifications/{notification_id}", json_data=_body(
            title=kwargs.get("title"), content=kwargs.get("content"),
            imageUrl=kwargs.get("image_url"),
        ))

    @async_require_login
    async def aupdate_notification(self, notification_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("PUT", f"/api/admin/notifications/{notification_id}", json_data=_body(
            title=kwargs.get("title"), content=kwargs.get("content"),
            imageUrl=kwargs.get("image_url"),
        ))

    @require_login
    def delete_notification(self, notification_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/notifications/{notification_id}")

    @async_require_login
    async def adelete_notification(self, notification_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/notifications/{notification_id}")

    @require_login
    def publish_notification(self, notification_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/notifications/{notification_id}/publish")

    @async_require_login
    async def apublish_notification(self, notification_id: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/notifications/{notification_id}/publish")

    # ======================================================================
    # Reports
    # ======================================================================

    @require_login
    def list_reports(self, page: Optional[int] = None, limit: Optional[int] = None, status: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/reports", params=_body(page=page, limit=limit, status=status))

    @async_require_login
    async def alist_reports(self, page: Optional[int] = None, limit: Optional[int] = None, status: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/reports", params=_body(page=page, limit=limit, status=status))

    @require_login
    def update_report(self, report_id: str, status: str, result: str) -> Dict[str, Any]:
        return self._http.request("PUT", f"/api/admin/reports/{report_id}", json_data={"status": status, "result": result})

    @async_require_login
    async def aupdate_report(self, report_id: str, status: str, result: str) -> Dict[str, Any]:
        return await self._http.arequest("PUT", f"/api/admin/reports/{report_id}", json_data={"status": status, "result": result})

