from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


# ============================================================================
# 用户
# ============================================================================


@dataclass
class User:
    """用户信息（来自登录/注册/个人资料接口）。"""

    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    intro: Optional[str] = None
    gender: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            email=data.get("email"),
            nickname=data.get("nickname"),
            avatar_url=data.get("avatar_url"),
            intro=data.get("intro"),
            gender=data.get("gender"),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.username is not None:
            result["username"] = self.username
        if self.email is not None:
            result["email"] = self.email
        if self.nickname is not None:
            result["nickname"] = self.nickname
        if self.avatar_url is not None:
            result["avatar_url"] = self.avatar_url
        if self.intro is not None:
            result["intro"] = self.intro
        if self.gender is not None:
            result["gender"] = self.gender
        if self.created_at is not None:
            result["created_at"] = self.created_at
        return result


# ============================================================================
# 用户简要信息（用于 FriendRequest / ContactDetail 等嵌套场景）
# ============================================================================


@dataclass
class UserInfo:
    """用户简要信息（嵌套在好友请求等响应中）。"""

    id: Optional[int] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInfo":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            nickname=data.get("nickname"),
            avatar_url=data.get("avatarUrl"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.username is not None:
            result["username"] = self.username
        if self.nickname is not None:
            result["nickname"] = self.nickname
        if self.avatar_url is not None:
            result["avatarUrl"] = self.avatar_url
        return result


# ============================================================================
# 附件（仅用于头像上传）
# ============================================================================


@dataclass
class Attachment:
    """头像上传响应。"""

    url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attachment":
        if not data:
            return cls()
        return cls(
            url=data.get("avatarUrl") or data.get("url"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.url is not None:
            result["avatarUrl"] = self.url
        return result


# ============================================================================
# 消息
# ============================================================================


@dataclass
class Message:
    """聊天消息（来自 GET /api/messages/:friendId 和 POST /api/messages/send）。"""

    id: Optional[int] = None
    sender_id: Optional[int] = None
    sender_name: Optional[str] = None
    receiver_id: Optional[int] = None
    content: Optional[str] = None
    msg_type: Optional[str] = None
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    is_read: Optional[int] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            sender_id=data.get("sender_id"),
            sender_name=data.get("sender_name"),
            receiver_id=data.get("receiver_id"),
            content=data.get("content"),
            msg_type=data.get("msg_type"),
            file_url=data.get("file_url"),
            file_name=data.get("file_name"),
            file_size=data.get("file_size"),
            is_read=data.get("is_read"),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.sender_id is not None:
            result["sender_id"] = self.sender_id
        if self.sender_name is not None:
            result["sender_name"] = self.sender_name
        if self.receiver_id is not None:
            result["receiver_id"] = self.receiver_id
        if self.content is not None:
            result["content"] = self.content
        if self.msg_type is not None:
            result["msg_type"] = self.msg_type
        if self.file_url is not None:
            result["file_url"] = self.file_url
        if self.file_name is not None:
            result["file_name"] = self.file_name
        if self.file_size is not None:
            result["file_size"] = self.file_size
        if self.is_read is not None:
            result["is_read"] = self.is_read
        if self.created_at is not None:
            result["created_at"] = self.created_at
        return result


# ============================================================================
# 联系人（好友列表项）
# ============================================================================


@dataclass
class Contact:
    """联系人列表项（来自 GET /api/contacts/list）。"""

    id: Optional[int] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[str] = None
    pinned: Optional[bool] = None
    friend_since: Optional[str] = None
    status: Optional[str] = None
    last_msg: Optional[str] = None
    last_msg_type: Optional[str] = None
    last_time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            nickname=data.get("nickname"),
            avatar_url=data.get("avatarUrl"),
            gender=data.get("gender"),
            pinned=data.get("pinned"),
            friend_since=data.get("friendSince"),
            status=data.get("status"),
            last_msg=data.get("lastMsg"),
            last_msg_type=data.get("lastMsgType"),
            last_time=data.get("lastTime"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.username is not None:
            result["username"] = self.username
        if self.nickname is not None:
            result["nickname"] = self.nickname
        if self.avatar_url is not None:
            result["avatarUrl"] = self.avatar_url
        if self.gender is not None:
            result["gender"] = self.gender
        if self.pinned is not None:
            result["pinned"] = self.pinned
        if self.friend_since is not None:
            result["friendSince"] = self.friend_since
        if self.status is not None:
            result["status"] = self.status
        if self.last_msg is not None:
            result["lastMsg"] = self.last_msg
        if self.last_msg_type is not None:
            result["lastMsgType"] = self.last_msg_type
        if self.last_time is not None:
            result["lastTime"] = self.last_time
        return result


# ============================================================================
# 好友关系记录
# ============================================================================


@dataclass
class FriendshipRecord:
    """好友关系记录（来自 ContactDetail 接口中的 friendship 字段）。"""

    id: Optional[int] = None
    user_id: Optional[int] = None
    friend_id: Optional[int] = None
    status: Optional[str] = None
    pinned: Optional[int] = None
    message: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FriendshipRecord":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            friend_id=data.get("friend_id"),
            status=data.get("status"),
            pinned=data.get("pinned"),
            message=data.get("message"),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.user_id is not None:
            result["user_id"] = self.user_id
        if self.friend_id is not None:
            result["friend_id"] = self.friend_id
        if self.status is not None:
            result["status"] = self.status
        if self.pinned is not None:
            result["pinned"] = self.pinned
        if self.message is not None:
            result["message"] = self.message
        if self.created_at is not None:
            result["created_at"] = self.created_at
        return result


# ============================================================================
# 联系人详情
# ============================================================================


@dataclass
class ContactDetail:
    """联系人详情（来自 GET /api/contacts/:id）。"""

    user: Optional[User] = None
    friendship: Optional[FriendshipRecord] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactDetail":
        if not data:
            return cls()
        user_data = data.get("user")
        friendship_data = data.get("friendship")
        return cls(
            user=User.from_dict(user_data) if user_data else None,
            friendship=FriendshipRecord.from_dict(friendship_data) if friendship_data else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.user is not None:
            result["user"] = self.user.to_dict()
        if self.friendship is not None:
            result["friendship"] = self.friendship.to_dict()
        return result


# ============================================================================
# 好友请求
# ============================================================================


@dataclass
class FriendRequest:
    """好友请求（来自 GET /api/contacts/requests）。"""

    id: Optional[int] = None
    user: Optional[UserInfo] = None
    message: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FriendRequest":
        if not data:
            return cls()
        user_data = data.get("user")
        return cls(
            id=data.get("id"),
            user=UserInfo.from_dict(user_data) if user_data else None,
            message=data.get("message"),
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.user is not None:
            result["user"] = self.user.to_dict()
        if self.message is not None:
            result["message"] = self.message
        if self.created_at is not None:
            result["createdAt"] = self.created_at
        return result


# ============================================================================
# 用户设置
# ============================================================================


@dataclass
class UserSettings:
    """用户设置（来自 GET /api/user/settings）。"""

    id: Optional[int] = None
    user_id: Optional[int] = None
    locale: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSettings":
        if not data:
            return cls()
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            locale=data.get("locale"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.user_id is not None:
            result["user_id"] = self.user_id
        if self.locale is not None:
            result["locale"] = self.locale
        return result


# ============================================================================
# 会话成员
# ============================================================================


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
            user_id=data.get("userId"),
            role=data.get("role"),
            muted=data.get("muted", False),
            banned=data.get("banned", False),
            joined_at=data.get("joinedAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.user_id is not None:
            result["userId"] = self.user_id
        if self.role is not None:
            result["role"] = self.role
        result["muted"] = self.muted
        result["banned"] = self.banned
        if self.joined_at is not None:
            result["joinedAt"] = self.joined_at
        return result


# ============================================================================
# 会话（私聊或群组）
# ============================================================================


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
    member_ids: list = field(default_factory=list)
    members: Optional[list] = None
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
            id=data.get("id"),
            kind=data.get("kind"),
            name=data.get("name"),
            topic=data.get("topic"),
            announcement=data.get("announcement"),
            is_private=data.get("isPrivate", False),
            icon=data.get("icon"),
            avatar_url=data.get("avatarUrl"),
            mute_all=data.get("muteAll", False),
            member_ids=data.get("memberIds", []),
            members=members,
            owner_id=data.get("ownerId"),
            created_at=data.get("createdAt"),
            last_message_id=data.get("lastMessageId"),
            last_message_at=data.get("lastMessageAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            result["id"] = self.id
        if self.kind is not None:
            result["kind"] = self.kind
        if self.name is not None:
            result["name"] = self.name
        if self.topic is not None:
            result["topic"] = self.topic
        if self.announcement is not None:
            result["announcement"] = self.announcement
        result["isPrivate"] = self.is_private
        if self.icon is not None:
            result["icon"] = self.icon
        if self.avatar_url is not None:
            result["avatarUrl"] = self.avatar_url
        result["muteAll"] = self.mute_all
        if self.member_ids:
            result["memberIds"] = self.member_ids
        if self.members is not None:
            result["members"] = [m.to_dict() for m in self.members]
        if self.owner_id is not None:
            result["ownerId"] = self.owner_id
        if self.created_at is not None:
            result["createdAt"] = self.created_at
        if self.last_message_id is not None:
            result["lastMessageId"] = self.last_message_id
        if self.last_message_at is not None:
            result["lastMessageAt"] = self.last_message_at
        return result


__all__ = [
    "User",
    "UserInfo",
    "Attachment",
    "Message",
    "Contact",
    "FriendshipRecord",
    "ContactDetail",
    "FriendRequest",
    "UserSettings",
    "ConversationMember",
    "Conversation",
]
