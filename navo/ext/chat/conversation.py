from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtConversationMixin:
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

