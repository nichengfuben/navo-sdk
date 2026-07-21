from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _omit_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class Organization:
    id: Optional[str] = None
    name: Optional[str] = None
    parent_id: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), name=data.get("name"),
            parent_id=data.get("parentId"), description=data.get("description"),
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "name": self.name, "parentId": self.parent_id,
            "description": self.description, "createdAt": self.created_at,
        })

@dataclass
class BootstrapData:
    """初始化数据。"""
    me: Optional[User] = None
    users: List[User] = field(default_factory=list)
    conversations: List[Conversation] = field(default_factory=list)
    friends: List[Friendship] = field(default_factory=list)
    friend_requests: List[FriendRequest] = field(default_factory=list)
    read_markers: Dict[str, str] = field(default_factory=dict)
    channel_read_states: Dict[str, Any] = field(default_factory=dict)
    last_messages: Dict[str, Message] = field(default_factory=dict)
    notifications: List[Notification] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BootstrapData":
        if not data:
            return cls()
        last_msgs = {}
        for conv_id, msg_data in data.get("lastMessages", {}).items():
            last_msgs[conv_id] = Message.from_dict(msg_data)
        return cls(
            me=User.from_dict(data.get("me", {})),
            users=[User.from_dict(u) for u in data.get("users", [])],
            conversations=[Conversation.from_dict(c) for c in data.get("conversations", [])],
            friends=[Friendship.from_dict(f) for f in data.get("friends", [])],
            friend_requests=[FriendRequest.from_dict(r) for r in data.get("friendRequests", [])],
            read_markers=data.get("readMarkers", {}),
            channel_read_states=data.get("channelReadStates", {}),
            last_messages=last_msgs,
            notifications=[Notification.from_dict(n) for n in data.get("notifications", [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "me": self.me.to_dict() if self.me else None,
            "users": [u.to_dict() for u in self.users],
            "conversations": [c.to_dict() for c in self.conversations],
            "friends": [f.to_dict() for f in self.friends],
            "friendRequests": [r.to_dict() for r in self.friend_requests],
            "readMarkers": self.read_markers,
            "channelReadStates": self.channel_read_states,
            "lastMessages": {k: v.to_dict() for k, v in self.last_messages.items()},
            "notifications": [n.to_dict() for n in self.notifications],
        }


__all__ = [
    "User", "Attachment", "Reaction", "MessageReplyTo", "Message",
    "ConversationPin", "ConversationMember", "Conversation",
    "Friendship", "FriendRequest", "Notification",
    "PollOption", "PollData", "PollResult",
    "ForwardedMessageItem", "ForwardedMessage",
    "Sticker", "StickerPack", "Organization", "BootstrapData",
]

