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


class ChannelRole(str, Enum):
    """群组角色。"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ConversationKind(str, Enum):
    """会话类型。"""
    DM = "dm"
    CHANNEL = "channel"


class ClientEventType(str, Enum):
    """WebSocket 客户端事件类型。"""
    AUTH = "auth"
    MESSAGE_SEND = "message:send"
    MESSAGE_RECALL = "message:recall"
    MESSAGE_EDIT = "message:edit"
    TYPING_START = "typing:start"
    TYPING_STOP = "typing:stop"
    PRESENCE_SET = "presence:set"
    REACTION_TOGGLE = "reaction:toggle"
    READ = "read"


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
    READY = "ready"
    ERROR = "error"
    MESSAGE_UPDATE = "message:update"
    TYPING = "typing"
    PRESENCE = "presence"
    USER_UPDATE = "user:update"
    CONVERSATION_NEW = "conversation:new"
    CONVERSATION_UPDATE = "conversation:update"
    CONVERSATION_REMOVE = "conversation:remove"
    HISTORY_CLEARED = "history:cleared"
    READ = "read"


__all__ = [
    "PresenceStatus",
    "Gender",
    "MessageKind",
    "FriendshipStatus",
    "ChannelRole",
    "ConversationKind",
    "ClientEventType",
    "ServerEventType",
]
