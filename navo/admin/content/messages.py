from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminMessagesMixin:
    # ======================================================================
    # Messages & audit
    # ======================================================================

    @require_login
    def delete_message(self, message_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/messages/{message_id}")

    @async_require_login
    async def adelete_message(self, message_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/messages/{message_id}")

    @require_login
    def list_messages(self, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/messages", params=_body(
            page=kwargs.get("page"), pageSize=kwargs.get("page_size"),
            authorId=kwargs.get("author_id"), kind=kwargs.get("kind"),
            search=kwargs.get("search"), conversationId=kwargs.get("conversation_id"),
            includeDeleted=kwargs.get("include_deleted"),
        ))

    @async_require_login
    async def alist_messages(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/messages", params=_body(
            page=kwargs.get("page"), pageSize=kwargs.get("page_size"),
            authorId=kwargs.get("author_id"), kind=kwargs.get("kind"),
            search=kwargs.get("search"), conversationId=kwargs.get("conversation_id"),
            includeDeleted=kwargs.get("include_deleted"),
        ))

    @require_login
    def list_audit_logs(self, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/audit-logs", params=_body(
            page=kwargs.get("page"), limit=kwargs.get("limit"),
            userId=kwargs.get("user_id"), action=kwargs.get("action"),
            targetType=kwargs.get("target_type"),
            startDate=kwargs.get("start_date"), endDate=kwargs.get("end_date"),
        ))

    @async_require_login
    async def alist_audit_logs(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/audit-logs", params=_body(
            page=kwargs.get("page"), limit=kwargs.get("limit"),
            userId=kwargs.get("user_id"), action=kwargs.get("action"),
            targetType=kwargs.get("target_type"),
            startDate=kwargs.get("start_date"), endDate=kwargs.get("end_date"),
        ))

