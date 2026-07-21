from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _omit_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class ForwardedMessageItem:
    message_id: Optional[str] = None
    author_id: Optional[str] = None
    author_name: Optional[str] = None
    kind: Optional[str] = None
    text: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ForwardedMessageItem":
        if not data:
            return cls()
        return cls(
            message_id=data.get("messageId"), author_id=data.get("authorId"),
            author_name=data.get("authorName"), kind=data.get("kind"),
            text=data.get("text"),
            attachments=[Attachment.from_dict(a) for a in data.get("attachments", [])],
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "messageId": self.message_id, "authorId": self.author_id,
            "authorName": self.author_name, "kind": self.kind, "text": self.text,
            "attachments": [a.to_dict() for a in self.attachments] or None,
            "createdAt": self.created_at,
        })

@dataclass
class ForwardedMessage:
    id: Optional[str] = None
    source_conv_id: Optional[str] = None
    title: Optional[str] = None
    items: List[ForwardedMessageItem] = field(default_factory=list)
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ForwardedMessage":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), source_conv_id=data.get("sourceConvId"),
            title=data.get("title"),
            items=[ForwardedMessageItem.from_dict(i) for i in data.get("items", [])],
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "sourceConvId": self.source_conv_id,
            "title": self.title,
            "items": [i.to_dict() for i in self.items] or None,
            "createdAt": self.created_at,
        })

@dataclass
class Sticker:
    id: Optional[str] = None
    pack_id: Optional[str] = None
    name: Optional[str] = None
    file_url: Optional[str] = None
    mime_type: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Sticker":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), pack_id=data.get("packId"),
            name=data.get("name"), file_url=data.get("fileUrl"),
            mime_type=data.get("mimeType"), created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "packId": self.pack_id, "name": self.name,
            "fileUrl": self.file_url, "mimeType": self.mime_type,
            "createdAt": self.created_at,
        })

@dataclass
class StickerPack:
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    stickers: List[Sticker] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StickerPack":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), name=data.get("name"),
            created_at=data.get("createdAt"), created_by=data.get("createdBy"),
            stickers=[Sticker.from_dict(s) for s in data.get("stickers", [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "name": self.name,
            "createdAt": self.created_at, "createdBy": self.created_by,
            "stickers": [s.to_dict() for s in self.stickers] or None,
        })

