from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

from navo.util.config import SDKConfig
from navo.util.container import Container
from navo.util.decorators import async_require_login, require_login
from navo.util.config import EnvManager
from navo.util.types.models import (
    Attachment, BootstrapData, Conversation, FriendRequest,
    Friendship, Message, User,
)
from navo.util.types.protocols import TokenStore
from navo.util.exceptions import AuthError, NavoError
from navo.util.transport import FileUploader, HTTPTransport, WebSocketTransport, setup_logging
from navo.captcha import solve_captcha_sync, asolve_captcha
from navo.extensions import NavoApiMixin
from navo.admin import NavoAdmin

_logger = logging.getLogger("navo")


class Navo(NavoApiMixin):
    """Navo IM SDK 主客户端。"""

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
        self._logger = setup_logging(level=self._config.log_level, fmt=self._config.log_format)
        self._me: Optional[User] = None
        self._bootstrap: Optional[BootstrapData] = None
        self._admin: Optional[NavoAdmin] = None

    @staticmethod
    def _build_config(config, base_url, ws_url, auto_refresh_token, debug):
        if config is not None:
            return config
        return SDKConfig(
            base_url=base_url or SDKConfig.base_url,
            ws_url=ws_url or SDKConfig.ws_url,
            auto_refresh_token=auto_refresh_token, debug=debug,
        )

    def _resolve_token_store(self, token_store):
        if token_store is not None:
            return token_store
        if self._container.has("token_store"):
            return self._container.resolve("token_store")
        return EnvManager()

    def _register_core_dependencies(self):
        self._container.register_singleton("config", self._config)
        self._container.register_singleton("token_store", self._token_store)

    @property
    def config(self) -> SDKConfig: return self._config
    @property
    def http(self) -> HTTPTransport: return self._http
    @property
    def ws(self) -> WebSocketTransport: return self._ws
    @property
    def uploader(self) -> FileUploader: return self._uploader
    @property
    def container(self) -> Container: return self._container
    @property
    def token_store(self) -> TokenStore: return self._token_store
    @property
    def me(self) -> Optional[User]: return self._me
    @property
    def bootstrap_data(self) -> Optional[BootstrapData]: return self._bootstrap

    @property
    def admin(self) -> NavoAdmin:
        if self._admin is None:
            self._admin = NavoAdmin(self)
        return self._admin

    def __enter__(self): return self
    def __exit__(self, *args): self.close()
    async def __aenter__(self): return self
    async def __aexit__(self, *args): await self.aclose()

    def close(self): self._http.close()
    async def aclose(self):
        await self._ws.stop()
        await self._http.aclose()

    # ======================================================================
    # 事件注册
    # ======================================================================

    def on_message(self, handler):
        self._ws.on("message:new", handler)
        return self

    def off_message(self, handler):
        self._ws.off("message:new", handler)
        return self

    def on_event(self, event_type, handler):
        self._ws.on(event_type, handler)
        return self

    async def listen(self):
        while self._ws._running:
            await asyncio.sleep(1)

    def listen_sync(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running(): raise NavoError("事件循环已在运行")
        except RuntimeError: pass
        loop = asyncio.new_event_loop()
        try: loop.run_until_complete(self.listen())
        except KeyboardInterrupt: pass
        finally: loop.close()

    async def start_listening(self): asyncio.create_task(self.listen())
    async def stop_listening(self): await self._ws.stop()

    # ======================================================================
    # 认证
    # ======================================================================

    def login(self, username: str, password: str) -> "Navo":
        captcha_token = solve_captcha_sync(self._config.pow_url)
        data = self._http.request("POST", "/api/auth/login", json_data={
            "username": username, "password": password,
            "captchaToken": captcha_token,
        })
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("登录成功: %s", username)
        return self

    async def alogin(self, username: str, password: str) -> "Navo":
        captcha_token = await asolve_captcha(self._config.pow_url)
        data = await self._http.arequest("POST", "/api/auth/login", json_data={
            "username": username, "password": password,
            "captchaToken": captcha_token,
        })
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("登录成功: %s", username)
        return self

    def register(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> "Navo":
        body: Dict[str, Any] = {
            "username": username, "password": password, "displayName": display_name,
        }
        for key, api_key in (
            ("type", "type"), ("email", "email"), ("phone", "phone"),
            ("code", "code"), ("captcha_token", "captchaToken"),
            ("invite_code", "inviteCode"),
        ):
            if kwargs.get(key) is not None:
                body[api_key] = kwargs[key]
        data = self._http.request("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("注册成功: %s", username)
        return self

    async def aregister(
        self, username: str, password: str, display_name: str, **kwargs: Any,
    ) -> "Navo":
        body: Dict[str, Any] = {
            "username": username, "password": password, "displayName": display_name,
        }
        for key, api_key in (
            ("type", "type"), ("email", "email"), ("phone", "phone"),
            ("code", "code"), ("captcha_token", "captchaToken"),
            ("invite_code", "inviteCode"),
        ):
            if kwargs.get(key) is not None:
                body[api_key] = kwargs[key]
        data = await self._http.arequest("POST", "/api/auth/register", json_data=body)
        self._token_store.save_token(data["token"])
        self._me = User.from_dict(data.get("user"))
        self._logger.info("注册成功: %s", username)
        return self

    # ======================================================================
    # 用户
    # ======================================================================

    @require_login
    def get_me(self) -> User:
        data = self._http.request("GET", "/api/me")
        self._me = User.from_dict(data)
        return self._me

    @async_require_login
    async def aget_me(self) -> User:
        data = await self._http.arequest("GET", "/api/me")
        self._me = User.from_dict(data)
        return self._me

    @require_login
    def update_profile(self, display_name=None, bio=None, gender=None,
                       avatar_url=None, avatar_color=None, require_friend_approval=None,
                       language=None) -> User:
        patch: Dict[str, Any] = {}
        if display_name is not None: patch["displayName"] = display_name
        if bio is not None: patch["bio"] = bio
        if gender is not None: patch["gender"] = gender
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if avatar_color is not None: patch["avatarColor"] = avatar_color
        if require_friend_approval is not None: patch["requireFriendApproval"] = require_friend_approval
        if language is not None: patch["language"] = language
        data = self._http.request("PATCH", "/api/me", json_data=patch)
        self._me = User.from_dict(data)
        return self._me

    @async_require_login
    async def aupdate_profile(self, display_name=None, bio=None, gender=None,
                              avatar_url=None, avatar_color=None, require_friend_approval=None,
                              language=None) -> User:
        patch: Dict[str, Any] = {}
        if display_name is not None: patch["displayName"] = display_name
        if bio is not None: patch["bio"] = bio
        if gender is not None: patch["gender"] = gender
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if avatar_color is not None: patch["avatarColor"] = avatar_color
        if require_friend_approval is not None: patch["requireFriendApproval"] = require_friend_approval
        if language is not None: patch["language"] = language
        data = await self._http.arequest("PATCH", "/api/me", json_data=patch)
        self._me = User.from_dict(data)
        return self._me

    @require_login
    def change_password(
        self, current_password: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> bool:
        body: Dict[str, Any] = {
            "currentPassword": current_password, "newPassword": new_password,
        }
        if captcha_token is not None:
            body["captchaToken"] = captcha_token
        self._http.request("POST", "/api/me/password", json_data=body)
        return True

    @async_require_login
    async def achange_password(
        self, current_password: str, new_password: str,
        captcha_token: Optional[str] = None,
    ) -> bool:
        body: Dict[str, Any] = {
            "currentPassword": current_password, "newPassword": new_password,
        }
        if captcha_token is not None:
            body["captchaToken"] = captcha_token
        await self._http.arequest("POST", "/api/me/password", json_data=body)
        return True

    @require_login
    def search_users(self, query: str) -> List[User]:
        data = self._http.request("GET", "/api/users/search", params={"q": query})
        return [User.from_dict(u) for u in data]

    @async_require_login
    async def asearch_users(self, query: str) -> List[User]:
        data = await self._http.arequest("GET", "/api/users/search", params={"q": query})
        return [User.from_dict(u) for u in data]

    # ======================================================================
    # Bootstrap
    # ======================================================================

    @require_login
    def bootstrap(self) -> BootstrapData:
        data = self._http.request("GET", "/api/bootstrap")
        self._bootstrap = BootstrapData.from_dict(data)
        return self._bootstrap

    @async_require_login
    async def abootstrap(self) -> BootstrapData:
        data = await self._http.arequest("GET", "/api/bootstrap")
        self._bootstrap = BootstrapData.from_dict(data)
        return self._bootstrap

    # ======================================================================
    # 会话
    # ======================================================================

    @require_login
    def get_conversations(self) -> List[Conversation]:
        data = self._http.request("GET", "/api/conversations")
        return [Conversation.from_dict(c) for c in data]

    @async_require_login
    async def aget_conversations(self) -> List[Conversation]:
        data = await self._http.arequest("GET", "/api/conversations")
        return [Conversation.from_dict(c) for c in data]

    @require_login
    def get_messages(self, conversation_id: str, limit: int = 200, **kwargs) -> List[Message]:
        params: Dict[str, Any] = {}
        if "before" in kwargs: params["before"] = kwargs["before"]
        if "since" in kwargs: params["since"] = kwargs["since"]
        if "cursor" in kwargs: params["cursor"] = kwargs["cursor"]
        if "page" in kwargs: params["page"] = kwargs["page"]
        if "page_size" in kwargs: params["pageSize"] = kwargs["page_size"]
        if not params:
            params["pageSize"] = limit
        data = self._http.request("GET", f"/api/conversations/{conversation_id}/messages", params=params)
        if isinstance(data, list):
            return [Message.from_dict(m) for m in data]
        return [Message.from_dict(m) for m in data.get("items", [])]

    @async_require_login
    async def aget_messages(self, conversation_id: str, limit: int = 200, **kwargs) -> List[Message]:
        params: Dict[str, Any] = {}
        if "before" in kwargs: params["before"] = kwargs["before"]
        if "since" in kwargs: params["since"] = kwargs["since"]
        if "cursor" in kwargs: params["cursor"] = kwargs["cursor"]
        if "page" in kwargs: params["page"] = kwargs["page"]
        if "page_size" in kwargs: params["pageSize"] = kwargs["page_size"]
        if not params:
            params["pageSize"] = limit
        data = await self._http.arequest("GET", f"/api/conversations/{conversation_id}/messages", params=params)
        if isinstance(data, list):
            return [Message.from_dict(m) for m in data]
        return [Message.from_dict(m) for m in data.get("items", [])]

    @require_login
    def clear_history(self, conversation_id: str) -> bool:
        self._http.request("DELETE", f"/api/conversations/{conversation_id}/messages")
        return True

    @async_require_login
    async def aclear_history(self, conversation_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/conversations/{conversation_id}/messages")
        return True

    # ======================================================================
    # 群组/频道管理
    # ======================================================================

    @require_login
    def create_channel(self, name: str, topic=None, is_private=None, icon=None, member_ids=None) -> Conversation:
        body: Dict[str, Any] = {"name": name}
        if topic is not None: body["topic"] = topic
        if is_private is not None: body["isPrivate"] = is_private
        if icon is not None: body["icon"] = icon
        if member_ids is not None: body["memberIds"] = member_ids
        data = self._http.request("POST", "/api/channels", json_data=body)
        return Conversation.from_dict(data)

    @async_require_login
    async def acreate_channel(self, name: str, topic=None, is_private=None, icon=None, member_ids=None) -> Conversation:
        body: Dict[str, Any] = {"name": name}
        if topic is not None: body["topic"] = topic
        if is_private is not None: body["isPrivate"] = is_private
        if icon is not None: body["icon"] = icon
        if member_ids is not None: body["memberIds"] = member_ids
        data = await self._http.arequest("POST", "/api/channels", json_data=body)
        return Conversation.from_dict(data)

    @require_login
    def update_channel(self, channel_id: str, name=None, topic=None, announcement=None,
                       icon=None, avatar_url=None, mute_all=None,
                       members_can_invite=None, is_private=None) -> Conversation:
        patch: Dict[str, Any] = {}
        if name is not None: patch["name"] = name
        if topic is not None: patch["topic"] = topic
        if announcement is not None: patch["announcement"] = announcement
        if icon is not None: patch["icon"] = icon
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if mute_all is not None: patch["muteAll"] = mute_all
        if members_can_invite is not None: patch["membersCanInvite"] = members_can_invite
        if is_private is not None: patch["isPrivate"] = is_private
        data = self._http.request("PATCH", f"/api/channels/{channel_id}", json_data=patch)
        return Conversation.from_dict(data)

    @async_require_login
    async def aupdate_channel(self, channel_id: str, name=None, topic=None, announcement=None,
                              icon=None, avatar_url=None, mute_all=None,
                              members_can_invite=None, is_private=None) -> Conversation:
        patch: Dict[str, Any] = {}
        if name is not None: patch["name"] = name
        if topic is not None: patch["topic"] = topic
        if announcement is not None: patch["announcement"] = announcement
        if icon is not None: patch["icon"] = icon
        if avatar_url is not None: patch["avatarUrl"] = avatar_url
        if mute_all is not None: patch["muteAll"] = mute_all
        if members_can_invite is not None: patch["membersCanInvite"] = members_can_invite
        if is_private is not None: patch["isPrivate"] = is_private
        data = await self._http.arequest("PATCH", f"/api/channels/{channel_id}", json_data=patch)
        return Conversation.from_dict(data)

    @require_login
    def delete_channel(self, channel_id: str) -> bool:
        self._http.request("DELETE", f"/api/channels/{channel_id}")
        return True

    @async_require_login
    async def adelete_channel(self, channel_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/channels/{channel_id}")
        return True

    @require_login
    def leave_channel(self, channel_id: str) -> bool:
        self._http.request("POST", f"/api/channels/{channel_id}/leave")
        return True

    @async_require_login
    async def aleave_channel(self, channel_id: str) -> bool:
        await self._http.arequest("POST", f"/api/channels/{channel_id}/leave")
        return True

    @require_login
    def create_dm(self, user_id: str) -> Conversation:
        data = self._http.request("POST", "/api/dms", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @async_require_login
    async def acreate_dm(self, user_id: str) -> Conversation:
        data = await self._http.arequest("POST", "/api/dms", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    # ======================================================================
    # 群组成员管理
    # ======================================================================

    @require_login
    def add_member(self, channel_id: str, user_id: str) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/members", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @async_require_login
    async def aadd_member(self, channel_id: str, user_id: str) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/members", json_data={"userId": user_id})
        return Conversation.from_dict(data)

    @require_login
    def remove_member(self, channel_id: str, user_id: str) -> Conversation:
        data = self._http.request("DELETE", f"/api/channels/{channel_id}/members/{user_id}")
        return Conversation.from_dict(data)

    @async_require_login
    async def aremove_member(self, channel_id: str, user_id: str) -> Conversation:
        data = await self._http.arequest("DELETE", f"/api/channels/{channel_id}/members/{user_id}")
        return Conversation.from_dict(data)

    @require_login
    def set_role(self, channel_id: str, user_id: str, role: str) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/role", json_data={"userId": user_id, "role": role})
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_role(self, channel_id: str, user_id: str, role: str) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/role", json_data={"userId": user_id, "role": role})
        return Conversation.from_dict(data)

    @require_login
    def set_muted(self, channel_id: str, user_id: str, muted: bool) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/mute", json_data={"userId": user_id, "muted": muted})
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_muted(self, channel_id: str, user_id: str, muted: bool) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/mute", json_data={"userId": user_id, "muted": muted})
        return Conversation.from_dict(data)

    @require_login
    def set_banned(self, channel_id: str, user_id: str, banned: bool) -> Conversation:
        data = self._http.request("POST", f"/api/channels/{channel_id}/ban", json_data={"userId": user_id, "banned": banned})
        return Conversation.from_dict(data)

    @async_require_login
    async def aset_banned(self, channel_id: str, user_id: str, banned: bool) -> Conversation:
        data = await self._http.arequest("POST", f"/api/channels/{channel_id}/ban", json_data={"userId": user_id, "banned": banned})
        return Conversation.from_dict(data)

    # ======================================================================
    # 好友系统
    # ======================================================================

    @require_login
    def send_friend_request(self, username: str, message: str = "") -> Dict[str, Any]:
        return self._http.request("POST", "/api/friends/request", json_data={"username": username, "message": message})

    @async_require_login
    async def asend_friend_request(self, username: str, message: str = "") -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/friends/request", json_data={"username": username, "message": message})

    @require_login
    def accept_friend_request(self, request_id: str) -> bool:
        self._http.request("POST", f"/api/friends/requests/{request_id}/accept")
        return True

    @async_require_login
    async def aaccept_friend_request(self, request_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/requests/{request_id}/accept")
        return True

    @require_login
    def decline_friend_request(self, request_id: str) -> bool:
        self._http.request("POST", f"/api/friends/requests/{request_id}/decline")
        return True

    @async_require_login
    async def adecline_friend_request(self, request_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/requests/{request_id}/decline")
        return True

    @require_login
    def remove_friend(self, user_id: str) -> bool:
        self._http.request("DELETE", f"/api/friends/{user_id}")
        return True

    @async_require_login
    async def aremove_friend(self, user_id: str) -> bool:
        await self._http.arequest("DELETE", f"/api/friends/{user_id}")
        return True

    @require_login
    def block_user(self, user_id: str) -> bool:
        self._http.request("POST", f"/api/friends/{user_id}/block")
        return True

    @async_require_login
    async def ablock_user(self, user_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/{user_id}/block")
        return True

    @require_login
    def unblock_user(self, user_id: str) -> bool:
        self._http.request("POST", f"/api/friends/{user_id}/unblock")
        return True

    @async_require_login
    async def aunblock_user(self, user_id: str) -> bool:
        await self._http.arequest("POST", f"/api/friends/{user_id}/unblock")
        return True

    @require_login
    def get_friendship(self, user_id: str) -> Friendship:
        data = self._http.request("GET", f"/api/friends/{user_id}")
        return Friendship.from_dict(data)

    @async_require_login
    async def aget_friendship(self, user_id: str) -> Friendship:
        data = await self._http.arequest("GET", f"/api/friends/{user_id}")
        return Friendship.from_dict(data)

    # ======================================================================
    # 文件上传
    # ======================================================================

    @require_login
    def upload_file(
        self, file_path: str, poster: Optional[str] = None,
        e2ee_conversation_id: Optional[str] = None,
    ) -> Attachment:
        return self._uploader.upload(file_path, poster=poster, e2ee_conversation_id=e2ee_conversation_id)

    @async_require_login
    async def aupload_file(
        self, file_path: str, poster: Optional[str] = None,
        e2ee_conversation_id: Optional[str] = None,
    ) -> Attachment:
        return await self._uploader.aupload(file_path, poster=poster, e2ee_conversation_id=e2ee_conversation_id)

    # ======================================================================
    # WebSocket 消息发送
    # ======================================================================

    async def ws_auth(self, token: Optional[str] = None) -> None:
        t = token or self._token_store.get_token()
        if not t: raise AuthError("请先登录")
        await self._ws.start(t)

    async def ws_send_message(self, conversation_id: str, text: str = "", kind: Optional[str] = None,
                              attachments: Optional[List[Attachment]] = None, card_id: Optional[str] = None,
                              reply_to_id: Optional[str] = None, client_id: Optional[str] = None,
                              fmt: Optional[str] = None, source_conv_id: Optional[str] = None,
                              forward_message_ids: Optional[List[str]] = None,
                              captcha_token: Optional[str] = None, sticker_id: Optional[str] = None,
                              scheduled_at: Optional[str] = None, e2ee: Optional[bool] = None,
                              e2ee_session_id: Optional[str] = None) -> None:
        payload: Dict[str, Any] = {"conversationId": conversation_id, "text": text}
        if kind: payload["kind"] = kind
        if fmt: payload["format"] = fmt
        if attachments: payload["attachments"] = [a.to_dict() for a in attachments]
        if card_id: payload["cardId"] = card_id
        if reply_to_id: payload["replyToId"] = reply_to_id
        if source_conv_id: payload["sourceConvId"] = source_conv_id
        if forward_message_ids: payload["forwardMessageIds"] = forward_message_ids
        if captcha_token: payload["captchaToken"] = captcha_token
        if sticker_id: payload["stickerId"] = sticker_id
        if scheduled_at: payload["scheduledAt"] = scheduled_at
        if e2ee is not None: payload["e2ee"] = e2ee
        if e2ee_session_id: payload["e2eeSessionId"] = e2ee_session_id
        event: Dict[str, Any] = {"type": "message:send", "payload": payload}
        if client_id: event["clientId"] = client_id
        await self._ws.send(event)

    async def ws_recall_message(self, message_id: str) -> None:
        await self._ws.send({"type": "message:recall", "messageId": message_id})

    async def ws_edit_message(self, message_id: str, text: str) -> None:
        await self._ws.send({"type": "message:edit", "messageId": message_id, "text": text})

    async def ws_typing_start(self, conversation_id: str) -> None:
        await self._ws.send({"type": "typing:start", "conversationId": conversation_id})

    async def ws_typing_stop(self, conversation_id: str) -> None:
        await self._ws.send({"type": "typing:stop", "conversationId": conversation_id})

    async def ws_set_presence(self, status: str) -> None:
        await self._ws.send({"type": "presence:set", "status": status})

    async def ws_toggle_reaction(self, message_id: str, emoji: str) -> None:
        await self._ws.send({"type": "reaction:toggle", "messageId": message_id, "emoji": emoji})

    async def ws_mark_read(self, conversation_id: str, message_id: str) -> None:
        await self._ws.send({"type": "read", "conversationId": conversation_id, "messageId": message_id})

    # ======================================================================
    # 健康检查
    # ======================================================================

    def health(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/health")

    async def ahealth(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/health")


__all__ = ["Navo"]
