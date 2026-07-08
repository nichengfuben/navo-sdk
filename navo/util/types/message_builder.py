from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.types.models import Attachment


class MessageBuilder:
    """消息构建器，对应 SendMessageRequest。"""

    def __init__(self, conversation_id: str) -> None:
        self._conversation_id = conversation_id
        self._kind: Optional[str] = None
        self._format: Optional[str] = None
        self._text: str = ""
        self._attachments: List[Attachment] = []
        self._card_id: Optional[str] = None
        self._reply_to_id: Optional[str] = None
        self._source_conv_id: Optional[str] = None
        self._forward_message_ids: Optional[List[str]] = None
        self._captcha_token: Optional[str] = None
        self._sticker_id: Optional[str] = None
        self._scheduled_at: Optional[str] = None
        self._e2ee: Optional[bool] = None
        self._e2ee_session_id: Optional[str] = None

    def text(self, text: str) -> "MessageBuilder":
        self._text = text
        if self._kind is None:
            self._kind = "text"
        return self

    def kind(self, kind: str) -> "MessageBuilder":
        self._kind = kind
        return self

    def format(self, fmt: str) -> "MessageBuilder":
        self._format = fmt
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

    def forward(self, source_conv_id: str, message_ids: List[str]) -> "MessageBuilder":
        self._source_conv_id = source_conv_id
        self._forward_message_ids = message_ids
        self._kind = "forwardedCard"
        return self

    def sticker(self, sticker_id: str) -> "MessageBuilder":
        self._sticker_id = sticker_id
        self._kind = "sticker"
        return self

    def scheduled_at(self, scheduled_at: str) -> "MessageBuilder":
        self._scheduled_at = scheduled_at
        return self

    def e2ee(self, enabled: bool = True, session_id: Optional[str] = None) -> "MessageBuilder":
        self._e2ee = enabled
        self._e2ee_session_id = session_id
        return self

    def captcha_token(self, token: str) -> "MessageBuilder":
        self._captcha_token = token
        return self

    def build(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"conversationId": self._conversation_id}
        if self._kind:
            payload["kind"] = self._kind
        if self._format:
            payload["format"] = self._format
        if self._text:
            payload["text"] = self._text
        if self._attachments:
            payload["attachments"] = [a.to_dict() for a in self._attachments]
        if self._card_id:
            payload["cardId"] = self._card_id
        if self._reply_to_id:
            payload["replyToId"] = self._reply_to_id
        if self._source_conv_id:
            payload["sourceConvId"] = self._source_conv_id
        if self._forward_message_ids:
            payload["forwardMessageIds"] = self._forward_message_ids
        if self._captcha_token:
            payload["captchaToken"] = self._captcha_token
        if self._sticker_id:
            payload["stickerId"] = self._sticker_id
        if self._scheduled_at:
            payload["scheduledAt"] = self._scheduled_at
        if self._e2ee is not None:
            payload["e2ee"] = self._e2ee
        if self._e2ee_session_id:
            payload["e2eeSessionId"] = self._e2ee_session_id
        return payload


__all__ = ["MessageBuilder"]
