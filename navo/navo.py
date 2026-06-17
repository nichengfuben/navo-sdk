from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

from navo.util.config import SDKConfig
from navo.util.container import Container
from navo.util.decorators import async_require_login, require_login
from navo.util.env import EnvManager
from navo.util.events import EventEmitter
from navo.util.exceptions import AuthError, NavoError
from navo.util.logging_util import setup_logging
from navo.util.models import (
    Attachment,
    Contact,
    ContactDetail,
    Conversation,
    FriendRequest,
    Message,
    User,
    UserSettings,
)
from navo.util.protocols import TokenStore
from navo.util.transport_http import HTTPTransport
from navo.util.transport_ws import WebSocketTransport
from navo.util.uploader import FileUploader

_logger = logging.getLogger("navo")


class Navo:
    """Navo IM SDK 主客户端。

    功能完整的即时通讯 SDK，支持：
    - 用户认证（登录/注册/修改密码/刷新令牌）
    - 用户资料管理（查看/更新/搜索/设置/头像）
    - 联系人管理（列表/详情/好友请求/拉黑/删除/置顶）
    - 消息收发（文本/文件/已读/撤回/未读统计）
    - WebSocket 实时消息监听

    使用示例::

        # 同步
        im = Navo().login("user", "pass")
        me = im.get_me()

        # 异步
        async with Navo() as im:
            await im.alogin("user", "pass")
            me = await im.aget_me()
    """

    def __init__(
        self,
        config: Optional[SDKConfig] = None,
        container: Optional[Container] = None,
        token_store: Optional[TokenStore] = None,
        base_url: Optional[str] = None,
        ws_url: Optional[str] = None,
        auto_refresh_token: bool = True,
        debug: bool = False,
    ) -> None:
        self._config = self._build_config(config, base_url, ws_url, auto_refresh_token, debug)
        self._container = container or Container()
        self._token_store = self._resolve_token_store(token_store)

        self._register_core_dependencies()

        self._http = HTTPTransport(self._config, self._token_store)
        self._container.register_singleton("http", self._http)

        self._ws = WebSocketTransport(self._config)
        self._container.register_singleton("ws", self._ws)

        self._uploader = FileUploader(self._http)
        self._container.register_singleton("uploader", self._uploader)

        self._logger = setup_logging(
            level=self._config.log_level,
            fmt=self._config.log_format,
        )

        # 用户信息缓存
        self._me: Optional[User] = None

    @staticmethod
    def _build_config(
        config: Optional[SDKConfig],
        base_url: Optional[str],
        ws_url: Optional[str],
        auto_refresh_token: bool,
        debug: bool,
    ) -> SDKConfig:
        if config is not None:
            return config
        return SDKConfig(
            base_url=base_url or SDKConfig.base_url,
            ws_url=ws_url or SDKConfig.ws_url,
            auto_refresh_token=auto_refresh_token,
            debug=debug,
        )

    def _resolve_token_store(self, token_store: Optional[TokenStore]) -> TokenStore:
        if token_store is not None:
            return token_store
        if self._container.has("token_store"):
            return self._container.resolve("token_store")
        env = EnvManager()
        return env

    def _register_core_dependencies(self) -> None:
        self._container.register_singleton("config", self._config)
        self._container.register_singleton("token_store", self._token_store)

    # ======================================================================
    # 属性
    # ======================================================================

    @property
    def config(self) -> SDKConfig:
        return self._config

    @property
    def http(self) -> HTTPTransport:
        return self._http

    @property
    def ws(self) -> WebSocketTransport:
        return self._ws

    @property
    def uploader(self) -> FileUploader:
        return self._uploader

    @property
    def container(self) -> Container:
        return self._container

    @property
    def token_store(self) -> TokenStore:
        return self._token_store

    @property
    def me(self) -> Optional[User]:
        return self._me

    # ======================================================================
    # 上下文管理器
    # ======================================================================

    def __enter__(self) -> "Navo":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    async def __aenter__(self) -> "Navo":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    def close(self) -> None:
        """关闭客户端，释放同步资源。"""
        self._http.close()

    async def aclose(self) -> None:
        """异步关闭客户端，释放所有资源。"""
        await self._ws.stop()
        await self._http.aclose()

    # ======================================================================
    # 事件注册
    # ======================================================================

    def on_message(self, handler: Callable[..., Any]) -> "Navo":
        """注册消息监听。handler 签名: handler(event: dict)。"""
        self._ws.on("new_message", handler)
        return self

    def off_message(self, handler: Callable[..., Any]) -> "Navo":
        """移除消息监听。"""
        self._ws.off("new_message", handler)
        return self

    def on_event(self, event_type: str, handler: Callable[..., Any]) -> "Navo":
        """注册任意 WebSocket 事件监听。"""
        self._ws.on(event_type, handler)
        return self

    async def listen(self) -> None:
        """异步阻塞监听（等待消息循环）。"""
        while self._ws._running:
            await asyncio.sleep(1)

    def listen_sync(self) -> None:
        """同步阻塞监听。"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise NavoError("事件循环已在运行，请使用 async listen()")
        except RuntimeError:
            pass
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self.listen())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    async def start_listening(self) -> None:
        """启动后台监听（非阻塞）。"""
        asyncio.create_task(self.listen())

    async def stop_listening(self) -> None:
        """停止后台监听。"""
        await self._ws.stop()

    # ======================================================================
    # WebSocket 消息发送
    # ======================================================================

    async def ws_auth(self, token: Optional[str] = None) -> None:
        """WebSocket 认证。"""
        t = token
        if t is None and hasattr(self._token_store, 'get_access_token'):
            t = self._token_store.get_access_token()
        if not t:
            t = self._token_store.get_token()
        if not t:
            raise AuthError("请先登录")
        await self._ws.start(t)

    async def ws_send_message(
        self,
        conversation_id: str,
        text: str = "",
        kind: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
        card_id: Optional[str] = None,
        reply_to_id: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> None:
        """通过 WebSocket 发送消息。"""
        payload: Dict[str, Any] = {"conversationId": conversation_id}
        if kind:
            payload["kind"] = kind
        if text:
            payload["text"] = text
        if attachments:
            payload["attachments"] = [a.to_dict() for a in attachments]
        if card_id:
            payload["cardId"] = card_id
        if reply_to_id:
            payload["replyToId"] = reply_to_id
        event: Dict[str, Any] = {
            "type": "message:send",
            "payload": payload,
        }
        if client_id:
            event["clientId"] = client_id
        await self._ws.send(event)

    async def ws_recall_message(self, message_id: str) -> None:
        """撤回消息。"""
        await self._ws.send({"type": "message:recall", "messageId": message_id})

    async def ws_edit_message(self, message_id: str, text: str) -> None:
        """编辑消息。"""
        await self._ws.send({"type": "message:edit", "messageId": message_id, "text": text})

    async def ws_typing_start(self, conversation_id: str) -> None:
        """开始输入。"""
        await self._ws.send({"type": "typing:start", "conversationId": conversation_id})

    async def ws_typing_stop(self, conversation_id: str) -> None:
        """停止输入。"""
        await self._ws.send({"type": "typing:stop", "conversationId": conversation_id})

    async def ws_set_presence(self, status: str) -> None:
        """设置在线状态。"""
        await self._ws.send({"type": "presence:set", "status": status})

    async def ws_toggle_reaction(self, message_id: str, emoji: str) -> None:
        """切换表情回应。"""
        await self._ws.send({"type": "reaction:toggle", "messageId": message_id, "emoji": emoji})

    async def ws_mark_read(self, conversation_id: str, message_id: str) -> None:
        """标记已读。"""
        await self._ws.send({
            "type": "read", "conversationId": conversation_id, "messageId": message_id,
        })

    # ======================================================================
    # 认证
    # ======================================================================

    def login(self, login: str, password: str) -> "Navo":
        """同步登录。login 可以是用户名或邮箱。"""
        data = self._http.request("POST", "/api/auth/login", json_data={
            "login": login, "password": password,
        })
        self._token_store.save_tokens(data["accessToken"], data["refreshToken"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("登录成功: %s", login)
        return self

    async def alogin(self, login: str, password: str) -> "Navo":
        """异步登录。"""
        data = await self._http.arequest("POST", "/api/auth/login", json_data={
            "login": login, "password": password,
        })
        self._token_store.save_tokens(data["accessToken"], data["refreshToken"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("登录成功: %s", login)
        return self

    def register(self, username: str, email: str, password: str) -> "Navo":
        """同步注册。"""
        data = self._http.request("POST", "/api/auth/register", json_data={
            "username": username, "email": email, "password": password,
        })
        self._token_store.save_tokens(data["accessToken"], data["refreshToken"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("注册成功: %s", username)
        return self

    async def aregister(self, username: str, email: str, password: str) -> "Navo":
        """异步注册。"""
        data = await self._http.arequest("POST", "/api/auth/register", json_data={
            "username": username, "email": email, "password": password,
        })
        self._token_store.save_tokens(data["accessToken"], data["refreshToken"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("注册成功: %s", username)
        return self

    def refresh_token(self, refresh_token: Optional[str] = None) -> str:
        """使用刷新令牌获取新的访问令牌。返回新的 accessToken。"""
        rt = refresh_token
        if rt is None and hasattr(self._token_store, 'get_refresh_token'):
            rt = self._token_store.get_refresh_token()
        if not rt:
            raise AuthError("缺少刷新令牌")
        data = self._http.request("POST", "/api/auth/refresh", json_data={
            "refreshToken": rt,
        })
        new_access = data["accessToken"]
        self._token_store.save_tokens(new_access, rt)
        return new_access

    async def arefresh_token(self, refresh_token: Optional[str] = None) -> str:
        """异步刷新令牌。"""
        rt = refresh_token
        if rt is None and hasattr(self._token_store, 'get_refresh_token'):
            rt = self._token_store.get_refresh_token()
        if not rt:
            raise AuthError("缺少刷新令牌")
        data = await self._http.arequest("POST", "/api/auth/refresh", json_data={
            "refreshToken": rt,
        })
        new_access = data["accessToken"]
        self._token_store.save_tokens(new_access, rt)
        return new_access

    # ======================================================================
    # 用户
    # ======================================================================

    @require_login
    def get_me(self) -> User:
        """获取当前用户信息。"""
        data = self._http.request("GET", "/api/user/profile")
        self._me = User.from_dict(data.get("user"))
        return self._me

    @async_require_login
    async def aget_me(self) -> User:
        """异步获取当前用户信息。"""
        data = await self._http.arequest("GET", "/api/user/profile")
        self._me = User.from_dict(data.get("user"))
        return self._me

    @require_login
    def update_profile(
        self,
        nickname: Optional[str] = None,
        intro: Optional[str] = None,
        gender: Optional[str] = None,
    ) -> User:
        """更新个人资料。"""
        body: Dict[str, Any] = {}
        if nickname is not None:
            body["nickname"] = nickname
        if intro is not None:
            body["intro"] = intro
        if gender is not None:
            body["gender"] = gender
        data = self._http.request("PUT", "/api/user/profile", json_data=body)
        self._me = User.from_dict(data.get("user"))
        return self._me

    @async_require_login
    async def aupdate_profile(
        self,
        nickname: Optional[str] = None,
        intro: Optional[str] = None,
        gender: Optional[str] = None,
    ) -> User:
        """异步更新个人资料。"""
        body: Dict[str, Any] = {}
        if nickname is not None:
            body["nickname"] = nickname
        if intro is not None:
            body["intro"] = intro
        if gender is not None:
            body["gender"] = gender
        data = await self._http.arequest("PUT", "/api/user/profile", json_data=body)
        self._me = User.from_dict(data.get("user"))
        return self._me

    @require_login
    def change_password(self, current_password: str, new_password: str) -> bool:
        """修改密码。"""
        self._http.request("PUT", "/api/user/password", json_data={
            "currentPassword": current_password, "newPassword": new_password,
        })
        return True

    @async_require_login
    async def achange_password(self, current_password: str, new_password: str) -> bool:
        """异步修改密码。"""
        await self._http.arequest("PUT", "/api/user/password", json_data={
            "currentPassword": current_password, "newPassword": new_password,
        })
        return True

    @require_login
    def search_users(self, query: str) -> List[User]:
        """搜索用户。"""
        data = self._http.request("GET", "/api/contacts/search", params={"q": query})
        return [User.from_dict(u) for u in data.get("users", [])]

    @async_require_login
    async def asearch_users(self, query: str) -> List[User]:
        """异步搜索用户。"""
        data = await self._http.arequest("GET", "/api/contacts/search", params={"q": query})
        return [User.from_dict(u) for u in data.get("users", [])]

    # ======================================================================
    # 用户设置
    # ======================================================================

    @require_login
    def get_settings(self) -> UserSettings:
        """获取用户设置。"""
        data = self._http.request("GET", "/api/user/settings")
        return UserSettings.from_dict(data.get("settings", {}))

    @async_require_login
    async def aget_settings(self) -> UserSettings:
        """异步获取用户设置。"""
        data = await self._http.arequest("GET", "/api/user/settings")
        return UserSettings.from_dict(data.get("settings", {}))

    @require_login
    def update_settings(self, **kwargs: Any) -> UserSettings:
        """更新用户设置。"""
        data = self._http.request("PUT", "/api/user/settings", json_data=kwargs)
        return UserSettings.from_dict(data.get("settings", {}))

    @async_require_login
    async def aupdate_settings(self, **kwargs: Any) -> UserSettings:
        """异步更新用户设置。"""
        data = await self._http.arequest("PUT", "/api/user/settings", json_data=kwargs)
        return UserSettings.from_dict(data.get("settings", {}))

    @require_login
    def update_locale(self, locale: str) -> str:
        """更新语言偏好。返回新的 locale 值。"""
        data = self._http.request("PUT", "/api/user/locale", json_data={"locale": locale})
        return data.get("locale", locale)

    @async_require_login
    async def aupdate_locale(self, locale: str) -> str:
        """异步更新语言偏好。"""
        data = await self._http.arequest("PUT", "/api/user/locale", json_data={"locale": locale})
        return data.get("locale", locale)

    @require_login
    def upload_avatar(self, file_path: str) -> Dict[str, Any]:
        """上传头像。返回 {"message", "avatarUrl", "user"}。"""
        return self._http.upload_file_sync("/api/user/avatar", file_path, field_name="avatar")

    @async_require_login
    async def aupload_avatar(self, file_path: str) -> Dict[str, Any]:
        """异步上传头像。"""
        return await self._http.upload_file_async("/api/user/avatar", file_path, field_name="avatar")

    # ======================================================================
    # 联系人
    # ======================================================================

    @require_login
    def get_contacts(self) -> List[Contact]:
        """获取好友列表。"""
        data = self._http.request("GET", "/api/contacts/list")
        return [Contact.from_dict(c) for c in data.get("contacts", [])]

    @async_require_login
    async def aget_contacts(self) -> List[Contact]:
        """异步获取好友列表。"""
        data = await self._http.arequest("GET", "/api/contacts/list")
        return [Contact.from_dict(c) for c in data.get("contacts", [])]

    @require_login
    def get_friend_requests(self) -> Dict[str, List[FriendRequest]]:
        """获取好友请求（发送的和接收的）。"""
        data = self._http.request("GET", "/api/contacts/requests")
        return {
            "sent": [FriendRequest.from_dict(r) for r in data.get("sent", [])],
            "received": [FriendRequest.from_dict(r) for r in data.get("received", [])],
        }

    @async_require_login
    async def aget_friend_requests(self) -> Dict[str, List[FriendRequest]]:
        """异步获取好友请求。"""
        data = await self._http.arequest("GET", "/api/contacts/requests")
        return {
            "sent": [FriendRequest.from_dict(r) for r in data.get("sent", [])],
            "received": [FriendRequest.from_dict(r) for r in data.get("received", [])],
        }

    @require_login
    def get_friend_request_count(self) -> int:
        """获取待处理好友请求数量。"""
        data = self._http.request("GET", "/api/contacts/requests/count")
        return data.get("count", 0)

    @async_require_login
    async def aget_friend_request_count(self) -> int:
        """异步获取待处理好友请求数量。"""
        data = await self._http.arequest("GET", "/api/contacts/requests/count")
        return data.get("count", 0)

    @require_login
    def send_friend_request(self, friend_id: int, message: str = "") -> Dict[str, Any]:
        """发送好友请求。"""
        return self._http.request("POST", "/api/contacts/request", json_data={
            "friendId": friend_id, "message": message,
        })

    @async_require_login
    async def asend_friend_request(self, friend_id: int, message: str = "") -> Dict[str, Any]:
        """异步发送好友请求。"""
        return await self._http.arequest("POST", "/api/contacts/request", json_data={
            "friendId": friend_id, "message": message,
        })

    @require_login
    def accept_friend_request(self, request_id: int) -> Dict[str, Any]:
        """接受好友请求。"""
        return self._http.request("POST", f"/api/contacts/accept/{request_id}")

    @async_require_login
    async def aaccept_friend_request(self, request_id: int) -> Dict[str, Any]:
        """异步接受好友请求。"""
        return await self._http.arequest("POST", f"/api/contacts/accept/{request_id}")

    @require_login
    def reject_friend_request(self, request_id: int) -> Dict[str, Any]:
        """拒绝好友请求。"""
        return self._http.request("POST", f"/api/contacts/reject/{request_id}")

    @async_require_login
    async def areject_friend_request(self, request_id: int) -> Dict[str, Any]:
        """异步拒绝好友请求。"""
        return await self._http.arequest("POST", f"/api/contacts/reject/{request_id}")

    @require_login
    def block_contact(self, user_id: int) -> Dict[str, Any]:
        """拉黑联系人。"""
        return self._http.request("POST", f"/api/contacts/block/{user_id}")

    @async_require_login
    async def ablock_contact(self, user_id: int) -> Dict[str, Any]:
        """异步拉黑联系人。"""
        return await self._http.arequest("POST", f"/api/contacts/block/{user_id}")

    @require_login
    def remove_friend(self, user_id: int) -> Dict[str, Any]:
        """删除好友。"""
        return self._http.request("DELETE", f"/api/contacts/{user_id}")

    @async_require_login
    async def aremove_friend(self, user_id: int) -> Dict[str, Any]:
        """异步删除好友。"""
        return await self._http.arequest("DELETE", f"/api/contacts/{user_id}")

    @require_login
    def toggle_pin(self, user_id: int) -> bool:
        """切换联系人置顶状态。返回新的 pinned 值。"""
        data = self._http.request("POST", f"/api/contacts/pin/{user_id}")
        return data.get("pinned", False)

    @async_require_login
    async def atoggle_pin(self, user_id: int) -> bool:
        """异步切换联系人置顶状态。"""
        data = await self._http.arequest("POST", f"/api/contacts/pin/{user_id}")
        return data.get("pinned", False)

    @require_login
    def get_contact(self, user_id: int) -> ContactDetail:
        """获取联系人详情。"""
        data = self._http.request("GET", f"/api/contacts/{user_id}")
        return ContactDetail.from_dict(data)

    @async_require_login
    async def aget_contact(self, user_id: int) -> ContactDetail:
        """异步获取联系人详情。"""
        data = await self._http.arequest("GET", f"/api/contacts/{user_id}")
        return ContactDetail.from_dict(data)

    # ======================================================================
    # 群组/频道管理
    # ======================================================================

    @require_login
    def get_conversations(self) -> List[Conversation]:
        """获取会话列表。"""
        data = self._http.request("GET", "/api/conversations")
        return [Conversation.from_dict(c) for c in data]

    @async_require_login
    async def aget_conversations(self) -> List[Conversation]:
        """异步获取会话列表。"""
        data = await self._http.arequest("GET", "/api/conversations")
        return [Conversation.from_dict(c) for c in data]

    @require_login
    def create_channel(
        self,
        name: str,
        topic: Optional[str] = None,
        is_private: Optional[bool] = None,
        icon: Optional[str] = None,
        member_ids: Optional[List[str]] = None,
    ) -> Conversation:
        """创建群组。"""
        body: Dict[str, Any] = {"name": name}
        if topic is not None:
            body["topic"] = topic
        if is_private is not None:
            body["isPrivate"] = is_private
        if icon is not None:
            body["icon"] = icon
        if member_ids is not None:
            body["memberIds"] = member_ids
        data = self._http.request("POST", "/api/channels", json_data=body)
        return Conversation.from_dict(data)

    @async_require_login
    async def acreate_channel(
        self,
        name: str,
        topic: Optional[str] = None,
        is_private: Optional[bool] = None,
        icon: Optional[str] = None,
        member_ids: Optional[List[str]] = None,
    ) -> Conversation:
        """异步创建群组。"""
        body: Dict[str, Any] = {"name": name}
        if topic is not None:
            body["topic"] = topic
        if is_private is not None:
            body["isPrivate"] = is_private
        if icon is not None:
            body["icon"] = icon
        if member_ids is not None:
            body["memberIds"] = member_ids
        data = await self._http.arequest("POST", "/api/channels", json_data=body)
        return Conversation.from_dict(data)

    @require_login
    def update_channel(
        self,
        channel_id: str,
        name: Optional[str] = None,
        topic: Optional[str] = None,
        announcement: Optional[str] = None,
        icon: Optional[str] = None,
        avatar_url: Optional[str] = None,
        mute_all: Optional[bool] = None,
    ) -> Conversation:
        """更新群组信息。"""
        patch: Dict[str, Any] = {}
        if name is not None:
            patch["name"] = name
        if topic is not None:
            patch["topic"] = topic
        if announcement is not None:
            patch["announcement"] = announcement
        if icon is not None:
            patch["icon"] = icon
        if avatar_url is not None:
            patch["avatarUrl"] = avatar_url
        if mute_all is not None:
            patch["muteAll"] = mute_all
        data = self._http.request("PATCH", f"/api/channels/{channel_id}", json_data=patch)
        return Conversation.from_dict(data)

    @async_require_login
    async def aupdate_channel(
        self,
        channel_id: str,
        name: Optional[str] = None,
        topic: Optional[str] = None,
        announcement: Optional[str] = None,
        icon: Optional[str] = None,
        avatar_url: Optional[str] = None,
        mute_all: Optional[bool] = None,
    ) -> Conversation:
        """异步更新群组信息。"""
        patch: Dict[str, Any] = {}
        if name is not None:
            patch["name"] = name
        if topic is not None:
            patch["topic"] = topic
        if announcement is not None:
            patch["announcement"] = announcement
        if icon is not None:
            patch["icon"] = icon
        if avatar_url is not None:
            patch["avatarUrl"] = avatar_url
        if mute_all is not None:
            patch["muteAll"] = mute_all
        data = await self._http.arequest("PATCH", f"/api/channels/{channel_id}", json_data=patch)
        return Conversation.from_dict(data)

    @require_login
    def create_dm(self, user_id: str) -> Conversation:
        """创建或获取私聊会话。"""
        data = self._http.request("POST", "/api/dms", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @async_require_login
    async def acreate_dm(self, user_id: str) -> Conversation:
        """异步创建或获取私聊会话。"""
        data = await self._http.arequest("POST", "/api/dms", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    # ======================================================================
    # 群组成员管理
    # ======================================================================

    @require_login
    def add_member(self, channel_id: str, user_id: str) -> Conversation:
        """添加群成员。"""
        data = self._http.request("POST", f"/api/channels/{channel_id}/members", json_data={
            "userId": user_id,
        })
        return Conversation.from_dict(data)

    @async_require_login
    async def aadd_member(self, channel_id: str, user_id: str) -> Conversation:
        """异步添加群成员。"""
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/members", json_data={
            "userId": user_id,
        })
        return Conversation.from_dict(data)

    @require_login
    def remove_member(self, channel_id: str, user_id: str) -> Conversation:
        """移除群成员。"""
        data = self._http.request("DELETE", f"/api/channels/{channel_id}/members/{user_id}")
        return Conversation.from_dict(data)

    @async_require_login
    async def aremove_member(self, channel_id: str, user_id: str) -> Conversation:
        """异步移除群成员。"""
        data = await self._http.arequest("DELETE", f"/api/channels/{channel_id}/members/{user_id}")
        return Conversation.from_dict(data)

    @require_login
    def set_role(self, channel_id: str, user_id: str, role: str) -> Conversation:
        """设置成员角色（admin/member）。"""
        data = self._http.request("POST", f"/api/channels/{channel_id}/role", json_data={
            "userId": user_id, "role": role,
        })
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_role(self, channel_id: str, user_id: str, role: str) -> Conversation:
        """异步设置成员角色。"""
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/role", json_data={
            "userId": user_id, "role": role,
        })
        return Conversation.from_dict(data)

    @require_login
    def set_muted(self, channel_id: str, user_id: str, muted: bool) -> Conversation:
        """设置成员禁言。"""
        data = self._http.request("POST", f"/api/channels/{channel_id}/mute", json_data={
            "userId": user_id, "muted": muted,
        })
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_muted(self, channel_id: str, user_id: str, muted: bool) -> Conversation:
        """异步设置成员禁言。"""
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/mute", json_data={
            "userId": user_id, "muted": muted,
        })
        return Conversation.from_dict(data)

    @require_login
    def set_banned(self, channel_id: str, user_id: str, banned: bool) -> Conversation:
        """设置成员封禁。"""
        data = self._http.request("POST", f"/api/channels/{channel_id}/ban", json_data={
            "userId": user_id, "banned": banned,
        })
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_banned(self, channel_id: str, user_id: str, banned: bool) -> Conversation:
        """异步设置成员封禁。"""
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/ban", json_data={
            "userId": user_id, "banned": banned,
        })
        return Conversation.from_dict(data)

    # ======================================================================
    # 消息
    # ======================================================================

    @require_login
    def get_messages(self, friend_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        """获取与好友的聊天记录。"""
        data = self._http.request("GET", f"/api/messages/{friend_id}", params={
            "limit": limit, "offset": offset,
        })
        return [Message.from_dict(m) for m in data.get("messages", [])]

    @async_require_login
    async def aget_messages(self, friend_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        """异步获取聊天记录。"""
        data = await self._http.arequest("GET", f"/api/messages/{friend_id}", params={
            "limit": limit, "offset": offset,
        })
        return [Message.from_dict(m) for m in data.get("messages", [])]

    @require_login
    def send_message(
        self,
        receiver_id: int,
        content: str = "",
        msg_type: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> Message:
        """发送消息。支持文本和文件。"""
        if file_path:
            data = self._http.upload_file_sync(
                "/api/messages/send", file_path, field_name="file",
                extra_data={"receiverId": str(receiver_id), "content": content, **({"msgType": msg_type} if msg_type else {})},
            )
        else:
            data = self._http.request("POST", "/api/messages/send", json_data={
                "receiverId": receiver_id, "content": content,
                **({"msgType": msg_type} if msg_type else {}),
            })
        return Message.from_dict(data.get("message", {}))

    @async_require_login
    async def asend_message(
        self,
        receiver_id: int,
        content: str = "",
        msg_type: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> Message:
        """异步发送消息。"""
        if file_path:
            data = await self._http.upload_file_async(
                "/api/messages/send", file_path, field_name="file",
                extra_data={"receiverId": str(receiver_id), "content": content, **({"msgType": msg_type} if msg_type else {})},
            )
        else:
            data = await self._http.arequest("POST", "/api/messages/send", json_data={
                "receiverId": receiver_id, "content": content,
                **({"msgType": msg_type} if msg_type else {}),
            })
        return Message.from_dict(data.get("message", {}))

    @require_login
    def mark_read(self, sender_id: int) -> int:
        """标记来自指定发送者的消息为已读。返回已读消息数。"""
        data = self._http.request("POST", f"/api/messages/read/{sender_id}")
        return data.get("count", 0)

    @async_require_login
    async def amark_read(self, sender_id: int) -> int:
        """异步标记已读。"""
        data = await self._http.arequest("POST", f"/api/messages/read/{sender_id}")
        return data.get("count", 0)

    @require_login
    def recall_message(self, message_id: int) -> Dict[str, Any]:
        """撤回消息（10分钟内）。"""
        return self._http.request("POST", f"/api/messages/recall/{message_id}")

    @async_require_login
    async def arecall_message(self, message_id: int) -> Dict[str, Any]:
        """异步撤回消息。"""
        return await self._http.arequest("POST", f"/api/messages/recall/{message_id}")

    @require_login
    def get_unread_count(self) -> Dict[str, int]:
        """获取未读消息数（按发送者分组）。"""
        data = self._http.request("GET", "/api/messages/unread/count")
        return data.get("counts", {})

    @async_require_login
    async def aget_unread_count(self) -> Dict[str, int]:
        """异步获取未读消息数。"""
        data = await self._http.arequest("GET", "/api/messages/unread/count")
        return data.get("counts", {})

    # ======================================================================
    # 健康检查（无需认证）
    # ======================================================================

    def health(self) -> Dict[str, Any]:
        """健康检查。"""
        return self._http.request("GET", "/api/health")

    async def ahealth(self) -> Dict[str, Any]:
        """异步健康检查。"""
        return await self._http.arequest("GET", "/api/health")


__all__ = ["Navo"]
