from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


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
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None: result["id"] = self.id
        if self.username is not None: result["username"] = self.username
        if self.display_name is not None: result["displayName"] = self.display_name
        if self.avatar_color is not None: result["avatarColor"] = self.avatar_color
        if self.avatar_url is not None: result["avatarUrl"] = self.avatar_url
        if self.bio is not None: result["bio"] = self.bio
        if self.gender is not None: result["gender"] = self.gender
        if self.status is not None: result["status"] = self.status
        if self.last_seen is not None: result["lastSeen"] = self.last_seen
        if self.require_friend_approval is not None: result["requireFriendApproval"] = self.require_friend_approval
        return result


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
    poster: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attachment":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), name=data.get("name"), url=data.get("url"),
            mime_type=data.get("mimeType"), size=data.get("size"),
            width=data.get("width"), height=data.get("height"),
            poster=data.get("poster"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None: result["id"] = self.id
        if self.name is not None: result["name"] = self.name
        if self.url is not None: result["url"] = self.url
        if self.mime_type is not None: result["mimeType"] = self.mime_type
        if self.size is not None: result["size"] = self.size
        if self.width is not None: result["width"] = self.width
        if self.height is not None: result["height"] = self.height
        if self.poster is not None: result["poster"] = self.poster
        return result


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


@dataclass
class Message:
    """聊天消息。"""
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    author_id: Optional[str] = None
    kind: Optional[str] = None
    text: Optional[str] = None
    card_id: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    reactions: List[Reaction] = field(default_factory=list)
    reply_to_id: Optional[str] = None
    edited_at: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            conversation_id=data.get("conversationId"),
            author_id=data.get("authorId"),
            kind=data.get("kind"),
            text=data.get("text"),
            card_id=data.get("cardId"),
            attachments=[Attachment.from_dict(a) for a in data.get("attachments", [])],
            reactions=[Reaction.from_dict(r) for r in data.get("reactions", [])],
            reply_to_id=data.get("replyToId"),
            edited_at=data.get("editedAt"),
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None: result["id"] = self.id
        if self.conversation_id is not None: result["conversationId"] = self.conversation_id
        if self.author_id is not None: result["authorId"] = self.author_id
        if self.kind is not None: result["kind"] = self.kind
        if self.text is not None: result["text"] = self.text
        if self.card_id is not None: result["cardId"] = self.card_id
        if self.attachments: result["attachments"] = [a.to_dict() for a in self.attachments]
        if self.reactions: result["reactions"] = [r.to_dict() for r in self.reactions]
        if self.reply_to_id is not None: result["replyToId"] = self.reply_to_id
        if self.edited_at is not None: result["editedAt"] = self.edited_at
        if self.created_at is not None: result["createdAt"] = self.created_at
        return result


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
        result: Dict[str, Any] = {}
        if self.user_id is not None: result["userId"] = self.user_id
        if self.role is not None: result["role"] = self.role
        result["muted"] = self.muted
        result["banned"] = self.banned
        if self.joined_at is not None: result["joinedAt"] = self.joined_at
        return result


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
    member_ids: List[str] = field(default_factory=list)
    members: Optional[List[ConversationMember]] = None
    owner_id: Optional[str] = None
    created_at: Optional[str] = None
    last_message_id: Optional[str] = None
    last_message_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        if not data:
            return cls()
        members_data = data.get("members")
        members = None
        if members_data is not None:
            members = [ConversationMember.from_dict(m) for m in members_data]
        return cls(
            id=data.get("id"), kind=data.get("kind"), name=data.get("name"),
            topic=data.get("topic"), announcement=data.get("announcement"),
            is_private=data.get("isPrivate", False), icon=data.get("icon"),
            avatar_url=data.get("avatarUrl"), mute_all=data.get("muteAll", False),
            member_ids=data.get("memberIds", []), members=members,
            owner_id=data.get("ownerId"), created_at=data.get("createdAt"),
            last_message_id=data.get("lastMessageId"), last_message_at=data.get("lastMessageAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None: result["id"] = self.id
        if self.kind is not None: result["kind"] = self.kind
        if self.name is not None: result["name"] = self.name
        if self.topic is not None: result["topic"] = self.topic
        if self.announcement is not None: result["announcement"] = self.announcement
        result["isPrivate"] = self.is_private
        if self.icon is not None: result["icon"] = self.icon
        if self.avatar_url is not None: result["avatarUrl"] = self.avatar_url
        result["muteAll"] = self.mute_all
        if self.member_ids: result["memberIds"] = self.member_ids
        if self.members is not None: result["members"] = [m.to_dict() for m in self.members]
        if self.owner_id is not None: result["ownerId"] = self.owner_id
        if self.created_at is not None: result["createdAt"] = self.created_at
        if self.last_message_id is not None: result["lastMessageId"] = self.last_message_id
        if self.last_message_at is not None: result["lastMessageAt"] = self.last_message_at
        return result


@dataclass
class Friendship:
    """好友关系。"""
    user_id: Optional[str] = None
    status: Optional[str] = None
    direction: Optional[str] = None
    blocked_by_me: bool = False
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Friendship":
        if not data:
            return cls()
        return cls(
            user_id=data.get("userId"), status=data.get("status"),
            direction=data.get("direction"), blocked_by_me=data.get("blockedByMe", False),
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.user_id is not None: result["userId"] = self.user_id
        if self.status is not None: result["status"] = self.status
        if self.direction is not None: result["direction"] = self.direction
        result["blockedByMe"] = self.blocked_by_me
        if self.created_at is not None: result["createdAt"] = self.created_at
        return result


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
        result: Dict[str, Any] = {}
        if self.id is not None: result["id"] = self.id
        if self.from_user_id is not None: result["fromUserId"] = self.from_user_id
        if self.to_user_id is not None: result["toUserId"] = self.to_user_id
        if self.message is not None: result["message"] = self.message
        if self.created_at is not None: result["createdAt"] = self.created_at
        return result


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
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.me: result["me"] = self.me.to_dict()
        result["users"] = [u.to_dict() for u in self.users]
        result["conversations"] = [c.to_dict() for c in self.conversations]
        result["friends"] = [f.to_dict() for f in self.friends]
        result["friendRequests"] = [r.to_dict() for r in self.friend_requests]
        result["readMarkers"] = self.read_markers
        result["channelReadStates"] = self.channel_read_states
        result["lastMessages"] = {k: v.to_dict() for k, v in self.last_messages.items()}
        return result


__all__ = [
    "User", "Attachment", "Reaction", "Message",
    "ConversationMember", "Conversation",
    "Friendship", "FriendRequest", "BootstrapData",
]
