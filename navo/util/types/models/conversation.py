from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _omit_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class ConversationPin:
    message_id: Optional[str] = None
    pinned_by: Optional[str] = None
    pinned_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationPin":
        if not data:
            return cls()
        return cls(
            message_id=data.get("messageId"),
            pinned_by=data.get("pinnedBy"),
            pinned_at=data.get("pinnedAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "messageId": self.message_id,
            "pinnedBy": self.pinned_by,
            "pinnedAt": self.pinned_at,
        })

@dataclass
class ConversationMember:
    """会话成员。"""
    user_id: Optional[str] = None
    role: Optional[str] = None
    muted: bool = False
    banned: bool = False
    joined_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationMember":
        if not data:
            return cls()
        return cls(
            user_id=data.get("userId"), role=data.get("role"),
            muted=data.get("muted", False), banned=data.get("banned", False),
            joined_at=data.get("joinedAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "userId": self.user_id, "role": self.role,
            "muted": self.muted, "banned": self.banned,
            "joinedAt": self.joined_at,
        })

@dataclass
class Conversation:
    """会话（私聊或群组）。"""
    id: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    topic: Optional[str] = None
    announcement: Optional[str] = None
    is_private: bool = False
    icon: Optional[str] = None
    avatar_url: Optional[str] = None
    mute_all: bool = False
    members_can_invite: Optional[bool] = None
    member_ids: List[str] = field(default_factory=list)
    members: Optional[List[ConversationMember]] = None
    owner_id: Optional[str] = None
    created_at: Optional[str] = None
    last_message_id: Optional[str] = None
    last_message_at: Optional[str] = None
    pinned: Optional[List[ConversationPin]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        if not data:
            return cls()
        members_data = data.get("members")
        members = None
        if members_data is not None:
            members = [ConversationMember.from_dict(m) for m in members_data]
        pinned_data = data.get("pinned")
        pinned = None
        if pinned_data is not None:
            pinned = [ConversationPin.from_dict(p) for p in pinned_data]
        return cls(
            id=data.get("id"), kind=data.get("kind"), name=data.get("name"),
            topic=data.get("topic"), announcement=data.get("announcement"),
            is_private=data.get("isPrivate", False), icon=data.get("icon"),
            avatar_url=data.get("avatarUrl"), mute_all=data.get("muteAll", False),
            members_can_invite=data.get("membersCanInvite"),
            member_ids=data.get("memberIds", []), members=members,
            owner_id=data.get("ownerId"), created_at=data.get("createdAt"),
            last_message_id=data.get("lastMessageId"),
            last_message_at=data.get("lastMessageAt"), pinned=pinned,
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "kind": self.kind, "name": self.name,
            "topic": self.topic, "announcement": self.announcement,
            "isPrivate": self.is_private, "icon": self.icon,
            "avatarUrl": self.avatar_url, "muteAll": self.mute_all,
            "membersCanInvite": self.members_can_invite,
            "memberIds": self.member_ids or None,
            "members": [m.to_dict() for m in self.members] if self.members else None,
            "ownerId": self.owner_id, "createdAt": self.created_at,
            "lastMessageId": self.last_message_id,
            "lastMessageAt": self.last_message_at,
            "pinned": [p.to_dict() for p in self.pinned] if self.pinned else None,
        })

