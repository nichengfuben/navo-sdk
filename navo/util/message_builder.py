from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.models import Attachment


class MessageBuilder:
    """消息构建器。"""

    def __init__(self, conversation_id: str) -> None:
        self._conversation_id = conversation_id
        self._kind: Optional[str] = None
        self._text: str = ""
        self._attachments: List[Attachment] = []
        self._card_id: Optional[str] = None
        self._reply_to_id: Optional[str] = None

    def text(self, text: str) -> "MessageBuilder":
        self._text = text
        if self._kind is None: self._kind = "text"
        return self

    def kind(self, kind: str) -> "MessageBuilder":
        self._kind = kind
        return self

    def attachment(self, att: Attachment) -> "MessageBuilder":
        self._attachments.append(att)
        return self

    def card(self, card_id: str, card_kind: str = "friendCard") -> "MessageBuilder":
        self._card_id = card_id
        self._kind = card_kind
        return self

    def reply_to(self, message_id: str) -> "MessageBuilder":
        self._reply_to_id = message_id
        return self

    def build(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"conversationId": self._conversation_id}
        if self._kind: payload["kind"] = self._kind
        if self._text: payload["text"] = self._text
        if self._attachments: payload["attachments"] = [a.to_dict() for a in self._attachments]
        if self._card_id: payload["cardId"] = self._card_id
        if self._reply_to_id: payload["replyToId"] = self._reply_to_id
        return payload


__all__ = ["MessageBuilder"]
