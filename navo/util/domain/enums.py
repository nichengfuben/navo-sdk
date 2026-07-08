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
    OTHER = "other"


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
    LOCATION = "location"
    FORWARDED_CARD = "forwardedCard"
    POLL = "poll"
    STICKER = "sticker"
    VOICE = "voice"


class MessageFormat(str, Enum):
    PLAIN = "plain"
    MARKDOWN = "markdown"


class ConversationKind(str, Enum):
    DM = "dm"
    CHANNEL = "channel"


class FriendshipStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"
    NONE = "none"


class FriendshipDirection(str, Enum):
    NONE = "none"
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class RegisterType(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    PHONE = "phone"


class CallKind(str, Enum):
    AUDIO = "audio"
    VIDEO = "video"


class CallTrackKind(str, Enum):
    CAMERA = "camera"
    SCREEN = "screen"


class SystemRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


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
    CALL_INVITE = "call:invite"
    CALL_ACCEPT = "call:accept"
    CALL_REJECT = "call:reject"
    CALL_CANCEL = "call:cancel"
    CALL_HANGUP = "call:hangup"
    CALL_OFFER = "call:offer"
    CALL_ANSWER = "call:answer"
    CALL_ICE = "call:ice"
    CALL_SUBSCRIBE = "call:subscribe"
    CALL_ADMIN = "call:admin"
    CALL_QUERY_ACTIVE = "call:query-active"
    POLL_VOTE = "poll:vote"
    PRESENCE_PING = "presence:ping"
    PRESENCE_PONG = "presence:pong"


class ServerEventType(str, Enum):
    READY = "ready"
    ERROR = "error"
    CAPTCHA_REQUIRED = "captcha_required"
    MESSAGE_NEW = "message:new"
    MESSAGE_UPDATE = "message:update"
    MESSAGE_SCHEDULED = "message:scheduled"
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
    CALL_INCOMING = "call:incoming"
    CALL_ACCEPTED = "call:accepted"
    CALL_REJECTED = "call:rejected"
    CALL_CANCELLED = "call:cancelled"
    CALL_HANGUP = "call:hangup"
    CALL_ANSWER = "call:answer"
    CALL_DOWNSTREAM_OFFER = "call:downstream-offer"
    CALL_ICE = "call:ice"
    CALL_PEER_JOINED = "call:peer-joined"
    CALL_PEER_LEFT = "call:peer-left"
    CALL_TRACK_PUBLISHED = "call:track-published"
    CALL_TRACK_UNPUBLISHED = "call:track-unpublished"
    CALL_ADMIN_EVENT = "call:admin-event"
    CALL_BANNED = "call:banned"
    CALL_ACTIVE_CALLS = "call:active-calls"
    USER_BANNED = "user:banned"
    NOTIFICATION_NEW = "notification:new"
    NOTIFICATION_UPDATE = "notification:update"
    NOTIFICATION_REMOVE = "notification:remove"
    POLL_UPDATE = "poll:update"
    E2EE_STARTED = "e2ee:started"
    E2EE_ENDED = "e2ee:ended"
    PRESENCE_PING = "presence:ping"
    PRESENCE_PONG = "presence:pong"


__all__ = [
    "PresenceStatus", "Gender", "ChannelRole", "MessageKind", "MessageFormat",
    "ConversationKind", "FriendshipStatus", "FriendshipDirection", "RegisterType",
    "CallKind", "CallTrackKind", "SystemRole",
    "ClientEventType", "ServerEventType",
]
