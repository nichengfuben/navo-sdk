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


@dataclass
class MessageReplyTo:
    id: Optional[str] = None
    text: Optional[str] = None
    author_id: Optional[str] = None
    author_name: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    kind: Optional[str] = None
    card_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageReplyTo":
        if not data:
            return cls()
        return cls(
            id=data.get("id"), text=data.get("text"),
            author_id=data.get("authorId"), author_name=data.get("authorName"),
            attachments=[Attachment.from_dict(a) for a in data.get("attachments", [])],
            kind=data.get("kind"), card_id=data.get("cardId"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "text": self.text, "authorId": self.author_id,
            "authorName": self.author_name,
            "attachments": [a.to_dict() for a in self.attachments] or None,
            "kind": self.kind, "cardId": self.card_id,
        })


@dataclass
class Message:
    """聊天消息。"""
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    author_id: Optional[str] = None
    kind: Optional[str] = None
    text: Optional[str] = None
    format: Optional[str] = None
    card_id: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    reactions: List[Reaction] = field(default_factory=list)
    reply_to_id: Optional[str] = None
    reply_to: Optional[MessageReplyTo] = None
    edited_at: Optional[str] = None
    created_at: Optional[str] = None
    scheduled_at: Optional[str] = None
    pending: Optional[bool] = None
    failed: Optional[bool] = None
    failed_reason: Optional[str] = None
    deleted: Optional[bool] = None
    sticker_id: Optional[str] = None
    e2ee: Optional[bool] = None
    e2ee_cleaned: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        if not data:
            return cls()
        reply_to = data.get("replyTo")
        return cls(
            id=data.get("id"),
            conversation_id=data.get("conversationId"),
            author_id=data.get("authorId"),
            kind=data.get("kind"),
            text=data.get("text"),
            format=data.get("format"),
            card_id=data.get("cardId"),
            attachments=[Attachment.from_dict(a) for a in data.get("attachments", [])],
            reactions=[Reaction.from_dict(r) for r in data.get("reactions", [])],
            reply_to_id=data.get("replyToId"),
            reply_to=MessageReplyTo.from_dict(reply_to) if reply_to else None,
            edited_at=data.get("editedAt"),
            created_at=data.get("createdAt"),
            scheduled_at=data.get("scheduledAt"),
            pending=data.get("pending"),
            failed=data.get("failed"),
            failed_reason=data.get("failedReason"),
            deleted=data.get("deleted"),
            sticker_id=data.get("stickerId"),
            e2ee=data.get("e2ee"),
            e2ee_cleaned=data.get("e2eeCleaned"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "id": self.id, "conversationId": self.conversation_id,
            "authorId": self.author_id, "kind": self.kind, "text": self.text,
            "format": self.format, "cardId": self.card_id,
            "attachments": [a.to_dict() for a in self.attachments] or None,
            "reactions": [r.to_dict() for r in self.reactions] or None,
            "replyToId": self.reply_to_id,
            "replyTo": self.reply_to.to_dict() if self.reply_to else None,
            "editedAt": self.edited_at, "createdAt": self.created_at,
            "scheduledAt": self.scheduled_at, "pending": self.pending,
            "failed": self.failed, "failedReason": self.failed_reason,
            "deleted": self.deleted, "stickerId": self.sticker_id,
            "e2ee": self.e2ee, "e2eeCleaned": self.e2ee_cleaned,
        })


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


@dataclass
class PollOption:
    id: Optional[str] = None
    text: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollOption":
        if not data:
            return cls()
        return cls(id=data.get("id"), text=data.get("text"))

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({"id": self.id, "text": self.text})


@dataclass
class PollData:
    question: Optional[str] = None
    options: List[PollOption] = field(default_factory=list)
    anonymous: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollData":
        if not data:
            return cls()
        return cls(
            question=data.get("question"),
            options=[PollOption.from_dict(o) for o in data.get("options", [])],
            anonymous=data.get("anonymous", False),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "question": self.question,
            "options": [o.to_dict() for o in self.options] or None,
            "anonymous": self.anonymous,
        })


@dataclass
class PollResult:
    option_id: Optional[str] = None
    text: Optional[str] = None
    count: int = 0
    voters: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PollResult":
        if not data:
            return cls()
        return cls(
            option_id=data.get("optionId"), text=data.get("text"),
            count=data.get("count", 0), voters=data.get("voters", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _omit_none({
            "optionId": self.option_id, "text": self.text,
            "count": self.count, "voters": self.voters or None,
        })


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
