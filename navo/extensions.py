from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from navo.util.decorators import async_require_login, require_login
from navo.util.domain.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)

if TYPE_CHECKING:
    from navo.util.transport.http import HTTPTransport
    from navo.util.transport.ws import WebSocketTransport


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class NavoApiMixin:
    """Navo IM 扩展 API（系统、认证、会话、E2EE、推送等）。"""

    _http: "HTTPTransport"
    _ws: "WebSocketTransport"
    _config: Any
    _token_store: Any
    _me: Optional[User]
    _uploader: Any

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

    # ======================================================================
    # 认证扩展
    # ======================================================================

    def send_verification_code(
        self, target: str, type_: str, purpose: str = "register",
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(target=target, type=type_, purpose=purpose, captchaToken=captcha_token)
        return self._http.request("POST", "/api/auth/verification-code", json_data=body)

    async def asend_verification_code(
        self, target: str, type_: str, purpose: str = "register",
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(target=target, type=type_, purpose=purpose, captchaToken=captcha_token)
        return await self._http.arequest("POST", "/api/auth/verification-code", json_data=body)

    def reset_password(
        self, target: str, type_: str, code: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(
            target=target, type=type_, code=code,
            newPassword=new_password, captchaToken=captcha_token,
        )
        return self._http.request("POST", "/api/auth/reset-password", json_data=body)

    async def areset_password(
        self, target: str, type_: str, code: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = _body(
            target=target, type=type_, code=code,
            newPassword=new_password, captchaToken=captcha_token,
        )
        return await self._http.arequest("POST", "/api/auth/reset-password", json_data=body)

    def verify_second_password(self, token: str, password: str) -> User:
        data = self._http.request("POST", "/api/auth/verify-second-password", json_data={
            "token": token, "password": password,
        })
        return User.from_dict(data.get("user", data))

    async def averify_second_password(self, token: str, password: str) -> User:
        data = await self._http.arequest("POST", "/api/auth/verify-second-password", json_data={
            "token": token, "password": password,
        })
        return User.from_dict(data.get("user", data))

    def sso_initiate(self) -> Dict[str, Any]:
        return self._http.request("POST", "/api/auth/sso/initiate")

    async def asso_initiate(self) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/auth/sso/initiate")

    def sso_login(self) -> Dict[str, Any]:
        return self._http.request("POST", "/api/auth/sso")

    async def asso_login(self) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/auth/sso")

    def register_extended(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> Dict[str, Any]:
        body = _body(
            username=username, password=password, displayName=display_name,
            type=kwargs.get("type"), email=kwargs.get("email"),
            phone=kwargs.get("phone"), code=kwargs.get("code"),
            captchaToken=kwargs.get("captcha_token"),
            inviteCode=kwargs.get("invite_code"),
        )
        data = self._http.request("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        return data

    async def aregister_extended(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> Dict[str, Any]:
        body = _body(
            username=username, password=password, displayName=display_name,
            type=kwargs.get("type"), email=kwargs.get("email"),
            phone=kwargs.get("phone"), code=kwargs.get("code"),
            captchaToken=kwargs.get("captcha_token"),
            inviteCode=kwargs.get("invite_code"),
        )
        data = await self._http.arequest("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        return data

    def logout(self) -> None:
        self._token_store.clear_token()
        self._me = None

    async def alogout(self) -> None:
        self.logout()

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

    # ======================================================================
    # 会话扩展
    # ======================================================================

    @require_login
    def get_conversation(self, conversation_id: str) -> Conversation:
        data = self._http.request("GET", f"/api/conversations/{conversation_id}")
        return Conversation.from_dict(data)

    @async_require_login
    async def aget_conversation(self, conversation_id: str) -> Conversation:
        data = await self._http.arequest("GET", f"/api/conversations/{conversation_id}")
        return Conversation.from_dict(data)

    @require_login
    def get_conversation_ban_status(self, conversation_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/conversations/{conversation_id}/ban-status")

    @async_require_login
    async def aget_conversation_ban_status(self, conversation_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/conversations/{conversation_id}/ban-status")

    @require_login
    def pin_message(self, conversation_id: str, message_id: str) -> bool:
        self._http.request("POST", f"/api/conversations/{conversation_id}/pin", json_data={"messageId": message_id})
        return True

    @async_require_login
    async def apin_message(self, conversation_id: str, message_id: str) -> bool:
        await self._http.arequest("POST", f"/api/conversations/{conversation_id}/pin", json_data={"messageId": message_id})
        return True

    @require_login
    def unpin_message(self, conversation_id: str, message_id: str) -> bool:
        self._http.request("DELETE", f"/api/conversations/{conversation_id}/pin/{message_id}")
        return True

    @async_require_login
    async def aunpin_message(self, conversation_id: str, message_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/conversations/{conversation_id}/pin/{message_id}")
        return True

    @require_login
    def get_pinned_messages(self, conversation_id: str) -> List[Message]:
        data = self._http.request("GET", f"/api/conversations/{conversation_id}/pins")
        return [Message.from_dict(m) for m in data.get("items", [])]

    @async_require_login
    async def aget_pinned_messages(self, conversation_id: str) -> List[Message]:
        data = await self._http.arequest("GET", f"/api/conversations/{conversation_id}/pins")
        return [Message.from_dict(m) for m in data.get("items", [])]

    @require_login
    def search_messages(
        self, conversation_id: str, query: Optional[str] = None,
        kind: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        params = _body(q=query, kind=kind, page=page, limit=limit)
        return self._http.request("GET", f"/api/conversations/{conversation_id}/messages/search", params=params)

    @async_require_login
    async def asearch_messages(
        self, conversation_id: str, query: Optional[str] = None,
        kind: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        params = _body(q=query, kind=kind, page=page, limit=limit)
        return await self._http.arequest("GET", f"/api/conversations/{conversation_id}/messages/search", params=params)

    @require_login
    def get_poll_results(self, conversation_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/conversations/{conversation_id}/poll-results")

    @async_require_login
    async def aget_poll_results(self, conversation_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/conversations/{conversation_id}/poll-results")

    @require_login
    def get_forwarded_message(self, forwarded_id: str) -> ForwardedMessage:
        data = self._http.request("GET", f"/api/forwarded/{forwarded_id}")
        return ForwardedMessage.from_dict(data)

    @async_require_login
    async def aget_forwarded_message(self, forwarded_id: str) -> ForwardedMessage:
        data = await self._http.arequest("GET", f"/api/forwarded/{forwarded_id}")
        return ForwardedMessage.from_dict(data)

    @require_login
    def list_public_channels(self, search: Optional[str] = None) -> List[Conversation]:
        params = _body(search=search)
        data = self._http.request("GET", "/api/channels/public", params=params or None)
        return [Conversation.from_dict(c) for c in data]

    @async_require_login
    async def alist_public_channels(self, search: Optional[str] = None) -> List[Conversation]:
        params = _body(search=search)
        data = await self._http.arequest("GET", "/api/channels/public", params=params or None)
        return [Conversation.from_dict(c) for c in data]

    # ======================================================================
    # 好友扩展
    # ======================================================================

    @require_login
    def set_friend_note(self, user_id: str, note: Optional[str] = None) -> bool:
        self._http.request("PATCH", f"/api/friends/{user_id}/note", json_data={"note": note})
        return True

    @async_require_login
    async def aset_friend_note(self, user_id: str, note: Optional[str] = None) -> bool:
        await self._http.arequest("PATCH", f"/api/friends/{user_id}/note", json_data={"note": note})
        return True

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

    # ======================================================================
    # E2EE
    # ======================================================================

    @require_login
    def upload_e2ee_prekey(
        self, identity_key: str, signed_pre_key: str, signed_pre_key_sig: str,
        one_time_pre_keys: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/me/e2ee/prekey", json_data=_body(
            identityKey=identity_key, signedPreKey=signed_pre_key,
            signedPreKeySig=signed_pre_key_sig, oneTimePreKeys=one_time_pre_keys,
        ))

    @async_require_login
    async def aupload_e2ee_prekey(
        self, identity_key: str, signed_pre_key: str, signed_pre_key_sig: str,
        one_time_pre_keys: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/me/e2ee/prekey", json_data=_body(
            identityKey=identity_key, signedPreKey=signed_pre_key,
            signedPreKeySig=signed_pre_key_sig, oneTimePreKeys=one_time_pre_keys,
        ))

    @require_login
    def get_user_e2ee_prekey(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/users/{user_id}/e2ee/prekey")

    @async_require_login
    async def aget_user_e2ee_prekey(self, user_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/users/{user_id}/e2ee/prekey")

    @require_login
    def save_e2ee_session(
        self, conversation_id: str, peer_id: str,
        session_id: Optional[str] = None, ratchet_state: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._http.request("POST", "/api/me/e2ee/sessions", json_data=_body(
            conversationId=conversation_id, peerId=peer_id,
            sessionId=session_id, ratchetState=ratchet_state,
        ))

    @async_require_login
    async def asave_e2ee_session(
        self, conversation_id: str, peer_id: str,
        session_id: Optional[str] = None, ratchet_state: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/me/e2ee/sessions", json_data=_body(
            conversationId=conversation_id, peerId=peer_id,
            sessionId=session_id, ratchetState=ratchet_state,
        ))

    @require_login
    def get_e2ee_session(self, conversation_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"/api/me/e2ee/sessions/{conversation_id}")

    @async_require_login
    async def aget_e2ee_session(self, conversation_id: str) -> Dict[str, Any]:
        return await self._http.arequest("GET", f"/api/me/e2ee/sessions/{conversation_id}")

    @require_login
    def delete_e2ee_session(self, conversation_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/me/e2ee/sessions/{conversation_id}", json_data=_body(reason=reason))

    @async_require_login
    async def adelete_e2ee_session(self, conversation_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest(
            "DELETE", f"/api/me/e2ee/sessions/{conversation_id}", json_data=_body(reason=reason),
        )

    # ======================================================================
    # WebSocket 扩展
    # ======================================================================

    async def ws_send_message_extended(
        self, payload: Dict[str, Any], client_id: Optional[str] = None,
    ) -> None:
        event: Dict[str, Any] = {"type": "message:send", "payload": payload}
        if client_id:
            event["clientId"] = client_id
        await self._ws.send(event)

    async def ws_poll_vote(self, message_id: str, option_id: str) -> None:
        await self._ws.send({"type": "poll:vote", "messageId": message_id, "optionId": option_id})

    async def ws_presence_ping(self, conversation_id: str) -> None:
        await self._ws.send({"type": "presence:ping", "conversationId": conversation_id})

    async def ws_presence_pong(self, conversation_id: str, ping_id: str, to_user_id: str) -> None:
        await self._ws.send({
            "type": "presence:pong",
            "conversationId": conversation_id,
            "pingId": ping_id,
            "toUserId": to_user_id,
        })

    async def ws_call_invite(self, call_id: str, conversation_id: str, kind: str) -> None:
        await self._ws.send({
            "type": "call:invite", "callId": call_id,
            "conversationId": conversation_id, "kind": kind,
        })

    async def ws_call_accept(self, call_id: str) -> None:
        await self._ws.send({"type": "call:accept", "callId": call_id})

    async def ws_call_reject(self, call_id: str) -> None:
        await self._ws.send({"type": "call:reject", "callId": call_id})

    async def ws_call_cancel(self, call_id: str) -> None:
        await self._ws.send({"type": "call:cancel", "callId": call_id})

    async def ws_call_hangup(self, call_id: str) -> None:
        await self._ws.send({"type": "call:hangup", "callId": call_id})

    async def ws_call_offer(self, call_id: str, sdp: str) -> None:
        await self._ws.send({"type": "call:offer", "callId": call_id, "sdp": sdp})

    async def ws_call_answer(
        self, call_id: str, subscriber_id: str, publisher_id: str, sdp: str,
    ) -> None:
        await self._ws.send({
            "type": "call:answer", "callId": call_id,
            "subscriberId": subscriber_id, "publisherId": publisher_id, "sdp": sdp,
        })

    async def ws_call_ice(
        self, call_id: str, candidate: Dict[str, Any],
        target: Optional[str] = None, subscriber_id: Optional[str] = None,
        publisher_id: Optional[str] = None,
    ) -> None:
        await self._ws.send(_body(
            type="call:ice", callId=call_id, candidate=candidate,
            target=target, subscriberId=subscriber_id, publisherId=publisher_id,
        ))

    async def ws_call_subscribe(self, call_id: str, publisher_id: str, kind: str) -> None:
        await self._ws.send({
            "type": "call:subscribe",
            "callId": call_id, "publisherId": publisher_id, "kind": kind,
        })

    async def ws_call_admin(self, call_id: str, action: str, user_id: str) -> None:
        await self._ws.send({
            "type": "call:admin", "callId": call_id, "action": action, "userId": user_id,
        })

    async def ws_call_query_active(self) -> None:
        await self._ws.send({"type": "call:query-active"})

    def off_event(self, event_type: str, handler) -> None:
        self._ws.off(event_type, handler)


__all__ = ["NavoApiMixin"]
