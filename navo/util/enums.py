from __future__ import annotations

from enum import Enum


class PresenceStatus(str, Enum):
    """在线状态。"""
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    BUSY = "busy"


class Gender(str, Enum):
    """性别。"""
    MALE = "male"
    FEMALE = "female"
    SECRET = "secret"


class MessageKind(str, Enum):
    """消息类型。"""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"


class FriendshipStatus(str, Enum):
    """好友关系状态。"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


class ServerEventType(str, Enum):
    """WebSocket 服务端事件类型。"""
    FRIEND_REQUEST = "friend_request"
    FRIEND_ACCEPTED = "friend_accepted"
    FRIEND_ACCEPTED_SELF = "friend_accepted_self"
    FRIEND_UPDATED = "friend_updated"
    FRIEND_REMOVED = "friend_removed"
    NEW_MESSAGE = "new_message"
    MESSAGE_SENT = "message_sent"
    MESSAGES_READ = "messages_read"
    MESSAGE_RECALLED = "message_recalled"


__all__ = [
    "PresenceStatus",
    "Gender",
    "MessageKind",
    "FriendshipStatus",
    "ServerEventType",
]
