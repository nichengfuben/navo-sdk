from __future__ import annotations

from enum import Enum


class PresenceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    BUSY = "busy"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"


class ChannelRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class MessageKind(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    AI = "ai"
    FRIEND_CARD = "friendCard"
    CHANNEL_CARD = "channelCard"
    SYSTEM = "system"


class ConversationKind(str, Enum):
    DM = "dm"
    CHANNEL = "channel"


class FriendshipStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


class FriendshipDirection(str, Enum):
    NONE = "none"
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class ClientEventType(str, Enum):
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
    READY = "ready"
    ERROR = "error"
    MESSAGE_NEW = "message:new"
    MESSAGE_UPDATE = "message:update"
    TYPING = "typing"
    PRESENCE = "presence"
    USER_UPDATE = "user:update"
    CONVERSATION_NEW = "conversation:new"
    CONVERSATION_UPDATE = "conversation:update"
    CONVERSATION_REMOVE = "conversation:remove"
    HISTORY_CLEARED = "history:cleared"
    READ = "read"
    FRIEND_REQUEST = "friend:request"
    FRIEND_UPDATE = "friend:update"
    FRIEND_REMOVE = "friend:remove"


__all__ = [
    "PresenceStatus", "Gender", "ChannelRole", "MessageKind",
    "ConversationKind", "FriendshipStatus", "FriendshipDirection",
    "ClientEventType", "ServerEventType",
]
