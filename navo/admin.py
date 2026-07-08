from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from navo.util.decorators import async_require_login, require_login

if TYPE_CHECKING:
    from navo.navo import Navo


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class NavoAdmin:
    """Navo IM 管理后台 API 客户端。"""

    def __init__(self, client: "Navo") -> None:
        self._client = client

    @property
    def _token_store(self):
        return self._client.token_store

    @property
    def _http(self):
        return self._client.http

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

    # ======================================================================
    # Settings & configs
    # ======================================================================

    @require_login
    def get_settings(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/settings")

    @async_require_login
    async def aget_settings(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/settings")

    @require_login
    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/settings", json_data=settings)

    @async_require_login
    async def aupdate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/settings", json_data=settings)

    @require_login
    def get_captcha_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/captcha-config")

    @async_require_login
    async def aget_captcha_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/captcha-config")

    @require_login
    def update_captcha_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/captcha-config", json_data=config)

    @async_require_login
    async def aupdate_captcha_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/captcha-config", json_data=config)

    @require_login
    def get_ai_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/ai-config")

    @async_require_login
    async def aget_ai_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/ai-config")

    @require_login
    def update_ai_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/ai-config", json_data=config)

    @async_require_login
    async def aupdate_ai_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/ai-config", json_data=config)

    @require_login
    def test_ai(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/ai-test", json_data=config)

    @async_require_login
    async def atest_ai(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/ai-test", json_data=config)

    @require_login
    def get_ice_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/ice-config")

    @async_require_login
    async def aget_ice_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/ice-config")

    @require_login
    def update_ice_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/ice-config", json_data=config)

    @async_require_login
    async def aupdate_ice_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/ice-config", json_data=config)

    @require_login
    def get_translation_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/translation-config")

    @async_require_login
    async def aget_translation_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/translation-config")

    @require_login
    def update_translation_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/translation-config", json_data=config)

    @async_require_login
    async def aupdate_translation_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/translation-config", json_data=config)

    @require_login
    def get_getui_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/getui-config")

    @async_require_login
    async def aget_getui_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/getui-config")

    @require_login
    def update_getui_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/getui-config", json_data=config)

    @async_require_login
    async def aupdate_getui_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/getui-config", json_data=config)

    @require_login
    def test_getui(self) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/getui-test")

    @async_require_login
    async def atest_getui(self) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/getui-test")

    @require_login
    def list_push_tokens(self) -> List[Dict[str, Any]]:
        return self._http.request("GET", "/api/admin/push-tokens")

    @async_require_login
    async def alist_push_tokens(self) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", "/api/admin/push-tokens")

    @require_login
    def get_sms_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/sms-config")

    @async_require_login
    async def aget_sms_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/sms-config")

    @require_login
    def update_sms_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/sms-config", json_data=config)

    @async_require_login
    async def aupdate_sms_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/sms-config", json_data=config)

    @require_login
    def test_sms(self, phone: str) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/sms-test", json_data={"phone": phone})

    @async_require_login
    async def atest_sms(self, phone: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/sms-test", json_data={"phone": phone})

    @require_login
    def get_email_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/email-config")

    @async_require_login
    async def aget_email_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/email-config")

    @require_login
    def update_email_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/email-config", json_data=config)

    @async_require_login
    async def aupdate_email_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/email-config", json_data=config)

    @require_login
    def test_email(self, email: str) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/email-test", json_data={"email": email})

    @async_require_login
    async def atest_email(self, email: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/email-test", json_data={"email": email})

    @require_login
    def get_nsfw_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/nsfw-config")

    @async_require_login
    async def aget_nsfw_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/nsfw-config")

    @require_login
    def update_nsfw_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/nsfw-config", json_data=config)

    @async_require_login
    async def aupdate_nsfw_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/nsfw-config", json_data=config)

    @require_login
    def get_sso_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/sso-config")

    @async_require_login
    async def aget_sso_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/sso-config")

    @require_login
    def update_sso_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/sso-config", json_data=config)

    @async_require_login
    async def aupdate_sso_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/sso-config", json_data=config)

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

    # ======================================================================
    # Sensitive words
    # ======================================================================

    @require_login
    def list_sensitive_words(self, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/sensitive-words", params=_body(
            page=kwargs.get("page"), pageSize=kwargs.get("page_size"),
            search=kwargs.get("search"), policy=kwargs.get("policy"),
        ))

    @async_require_login
    async def alist_sensitive_words(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/sensitive-words", params=_body(
            page=kwargs.get("page"), pageSize=kwargs.get("page_size"),
            search=kwargs.get("search"), policy=kwargs.get("policy"),
        ))

    @require_login
    def add_sensitive_words(self, words: List[str], policy: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/sensitive-words", json_data=_body(words=words, policy=policy))

    @async_require_login
    async def aadd_sensitive_words(self, words: List[str], policy: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/sensitive-words", json_data=_body(words=words, policy=policy))

    @require_login
    def delete_sensitive_words(self, ids: List[str]) -> Dict[str, Any]:
        return self._http.request("DELETE", "/api/admin/sensitive-words", json_data={"ids": ids})

    @async_require_login
    async def adelete_sensitive_words(self, ids: List[str]) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", "/api/admin/sensitive-words", json_data={"ids": ids})

    # ======================================================================
    # Sticker packs (admin)
    # ======================================================================

    @require_login
    def create_sticker_pack(self, name: str) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/sticker-packs", json_data={"name": name})

    @async_require_login
    async def acreate_sticker_pack(self, name: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/sticker-packs", json_data={"name": name})

    @require_login
    def update_sticker_pack(self, pack_id: str, name: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"/api/admin/sticker-packs/{pack_id}", json_data={"name": name})

    @async_require_login
    async def aupdate_sticker_pack(self, pack_id: str, name: str) -> Dict[str, Any]:
        return await self._http.arequest("PATCH", f"/api/admin/sticker-packs/{pack_id}", json_data={"name": name})

    @require_login
    def delete_sticker_pack(self, pack_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/sticker-packs/{pack_id}")

    @async_require_login
    async def adelete_sticker_pack(self, pack_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/sticker-packs/{pack_id}")

    @require_login
    def add_sticker(self, pack_id: str, name: str, file_url: str, mime_type: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/sticker-packs/{pack_id}/stickers", json_data=_body(
            name=name, fileUrl=file_url, mimeType=mime_type,
        ))

    @async_require_login
    async def aadd_sticker(self, pack_id: str, name: str, file_url: str, mime_type: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/sticker-packs/{pack_id}/stickers", json_data=_body(
            name=name, fileUrl=file_url, mimeType=mime_type,
        ))

    @require_login
    def update_sticker(self, pack_id: str, sticker_id: str, name: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}", json_data={"name": name})

    @async_require_login
    async def aupdate_sticker(self, pack_id: str, sticker_id: str, name: str) -> Dict[str, Any]:
        return await self._http.arequest("PATCH", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}", json_data={"name": name})

    @require_login
    def delete_sticker(self, pack_id: str, sticker_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}")

    @async_require_login
    async def adelete_sticker(self, pack_id: str, sticker_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}")

    # ======================================================================
    # Whitelists
    # ======================================================================

    @require_login
    def list_email_whitelist(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/email-whitelist")

    @async_require_login
    async def alist_email_whitelist(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/email-whitelist")

    @require_login
    def add_email_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/email-whitelist", json_data=_body(pattern=pattern, note=note))

    @async_require_login
    async def aadd_email_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/email-whitelist", json_data=_body(pattern=pattern, note=note))

    @require_login
    def delete_email_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/email-whitelist/{entry_id}")

    @async_require_login
    async def adelete_email_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/email-whitelist/{entry_id}")

    @require_login
    def list_phone_whitelist(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/phone-whitelist")

    @async_require_login
    async def alist_phone_whitelist(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/phone-whitelist")

    @require_login
    def add_phone_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/phone-whitelist", json_data=_body(pattern=pattern, note=note))

    @async_require_login
    async def aadd_phone_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/phone-whitelist", json_data=_body(pattern=pattern, note=note))

    @require_login
    def delete_phone_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/phone-whitelist/{entry_id}")

    @async_require_login
    async def adelete_phone_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/phone-whitelist/{entry_id}")


__all__ = ["NavoAdmin"]
