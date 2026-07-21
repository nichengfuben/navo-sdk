from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtWsMixin:
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
