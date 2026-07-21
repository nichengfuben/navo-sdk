from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtMiscMixin:
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

