from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _omit_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class User:
    """用户信息。"""
    id: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    avatar_color: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    status: Optional[str] = None
    last_seen: Optional[str] = None
    require_friend_approval: Optional[bool] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    organization_id: Optional[str] = None
    org_title: Optional[str] = None
    language: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            display_name=data.get("displayName"),
            avatar_color=data.get("avatarColor"),
            avatar_url=data.get("avatarUrl"),
            bio=data.get("bio"),
            gender=data.get("gender"),
            status=data.get("status"),
            last_seen=data.get("lastSeen"),
            require_friend_approval=data.get("requireFriendApproval"),
            email=data.get("email"),
            phone=data.get("phone"),
            organization_id=data.get("organizationId"),
            org_title=data.get("orgTitle"),
            language=data.get("language"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id,
            "username": self.username,
            "displayName": self.display_name,
            "avatarColor": self.avatar_color,
            "avatarUrl": self.avatar_url,
            "bio": self.bio,
            "gender": self.gender,
            "status": self.status,
            "lastSeen": self.last_seen,
            "requireFriendApproval": self.require_friend_approval,
            "email": self.email,
            "phone": self.phone,
            "organizationId": self.organization_id,
            "orgTitle": self.org_title,
            "language": self.language,
        })

@dataclass
class Attachment:
    """消息附件。"""
    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None
    poster: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attachment":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), name=data.get("name"), url=data.get("url"),
            mime_type=data.get("mimeType"), size=data.get("size"),
            width=data.get("width"), height=data.get("height"),
            duration=data.get("duration"), poster=data.get("poster"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "name": self.name, "url": self.url,
            "mimeType": self.mime_type, "size": self.size,
            "width": self.width, "height": self.height,
            "duration": self.duration, "poster": self.poster,
        })

@dataclass
class Reaction:
    """消息表情回应。"""
    emoji: Optional[str] = None
    user_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reaction":
        if not data:
            return cls()
        return cls(emoji=data.get("emoji"), user_ids=data.get("userIds", []))

    def to_dict(self) -> Dict[str, Any]:
        return {"emoji": self.emoji, "userIds": self.user_ids}

