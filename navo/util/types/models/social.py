from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _omit_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class Friendship:
    """好友关系。"""
    user_id: Optional[str] = None
    status: Optional[str] = None
    direction: Optional[str] = None
    blocked_by_me: bool = False
    created_at: Optional[str] = None
    note: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Friendship":
        if not data:
            return cls()
        return cls(
            user_id=data.get("userId"), status=data.get("status"),
            direction=data.get("direction"), blocked_by_me=data.get("blockedByMe", False),
            created_at=data.get("createdAt"), note=data.get("note"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "userId": self.user_id, "status": self.status,
            "direction": self.direction, "blockedByMe": self.blocked_by_me,
            "createdAt": self.created_at, "note": self.note,
        })

@dataclass
class FriendRequest:
    """好友请求。"""
    id: Optional[str] = None
    from_user_id: Optional[str] = None
    to_user_id: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FriendRequest":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), from_user_id=data.get("fromUserId"),
            to_user_id=data.get("toUserId"), message=data.get("message"),
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "fromUserId": self.from_user_id,
            "toUserId": self.to_user_id, "message": self.message,
            "createdAt": self.created_at,
        })

@dataclass
class Notification:
    id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    author_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    target_user_id: Optional[str] = None
    read: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notification":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), title=data.get("title"), content=data.get("content"),
            image_url=data.get("imageUrl"), author_id=data.get("authorId"),
            created_at=data.get("createdAt"), updated_at=data.get("updatedAt"),
            target_user_id=data.get("targetUserId"), read=data.get("read"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "title": self.title, "content": self.content,
            "imageUrl": self.image_url, "authorId": self.author_id,
            "createdAt": self.created_at, "updatedAt": self.updated_at,
            "targetUserId": self.target_user_id, "read": self.read,
        })

