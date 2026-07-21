from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _omit_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class MessageReplyTo:
    id: Optional[str] = None
    text: Optional[str] = None
    author_id: Optional[str] = None
    author_name: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    kind: Optional[str] = None
    card_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageReplyTo":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), text=data.get("text"),
            author_id=data.get("authorId"), author_name=data.get("authorName"),
            attachments=[Attachment.from_dict(a) for a in data.get("attachments", [])],
            kind=data.get("kind"), card_id=data.get("cardId"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "text": self.text, "authorId": self.author_id,
            "authorName": self.author_name,
            "attachments": [a.to_dict() for a in self.attachments] or None,
            "kind": self.kind, "cardId": self.card_id,
        })

@dataclass
class Message:
    """聊天消息。"""
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    author_id: Optional[str] = None
    kind: Optional[str] = None
    text: Optional[str] = None
    format: Optional[str] = None
    card_id: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    reactions: List[Reaction] = field(default_factory=list)
    reply_to_id: Optional[str] = None
    reply_to: Optional[MessageReplyTo] = None
    edited_at: Optional[str] = None
    created_at: Optional[str] = None
    scheduled_at: Optional[str] = None
    pending: Optional[bool] = None
    failed: Optional[bool] = None
    failed_reason: Optional[str] = None
    deleted: Optional[bool] = None
    sticker_id: Optional[str] = None
    e2ee: Optional[bool] = None
    e2ee_cleaned: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        if not data:
            return cls()
        reply_to = data.get("replyTo")
        return cls(
            id=data.get("id"),
            conversation_id=data.get("conversationId"),
            author_id=data.get("authorId"),
            kind=data.get("kind"),
            text=data.get("text"),
            format=data.get("format"),
            card_id=data.get("cardId"),
            attachments=[Attachment.from_dict(a) for a in data.get("attachments", [])],
            reactions=[Reaction.from_dict(r) for r in data.get("reactions", [])],
            reply_to_id=data.get("replyToId"),
            reply_to=MessageReplyTo.from_dict(reply_to) if reply_to else None,
            edited_at=data.get("editedAt"),
            created_at=data.get("createdAt"),
            scheduled_at=data.get("scheduledAt"),
            pending=data.get("pending"),
            failed=data.get("failed"),
            failed_reason=data.get("failedReason"),
            deleted=data.get("deleted"),
            sticker_id=data.get("stickerId"),
            e2ee=data.get("e2ee"),
            e2ee_cleaned=data.get("e2eeCleaned"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "conversationId": self.conversation_id,
            "authorId": self.author_id, "kind": self.kind, "text": self.text,
            "format": self.format, "cardId": self.card_id,
            "attachments": [a.to_dict() for a in self.attachments] or None,
            "reactions": [r.to_dict() for r in self.reactions] or None,
            "replyToId": self.reply_to_id,
            "replyTo": self.reply_to.to_dict() if self.reply_to else None,
            "editedAt": self.edited_at, "createdAt": self.created_at,
            "scheduledAt": self.scheduled_at, "pending": self.pending,
            "failed": self.failed, "failedReason": self.failed_reason,
            "deleted": self.deleted, "stickerId": self.sticker_id,
            "e2ee": self.e2ee, "e2eeCleaned": self.e2ee_cleaned,
        })

@dataclass
class PollOption:
    id: Optional[str] = None
    text: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollOption":
        if not data:
            return cls()
        return cls(id=data.get("id"), text=data.get("text"))

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({"id": self.id, "text": self.text})

@dataclass
class PollData:
    question: Optional[str] = None
    options: List[PollOption] = field(default_factory=list)
    anonymous: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollData":
        if not data:
            return cls()
        return cls(
            question=data.get("question"),
            options=[PollOption.from_dict(o) for o in data.get("options", [])],
            anonymous=data.get("anonymous", False),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "question": self.question,
            "options": [o.to_dict() for o in self.options] or None,
            "anonymous": self.anonymous,
        })

@dataclass
class PollResult:
    option_id: Optional[str] = None
    text: Optional[str] = None
    count: int = 0
    voters: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollResult":
        if not data:
            return cls()
        return cls(
            option_id=data.get("optionId"), text=data.get("text"),
            count=data.get("count", 0), voters=data.get("voters", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "optionId": self.option_id, "text": self.text,
            "count": self.count, "voters": self.voters or None,
        })

