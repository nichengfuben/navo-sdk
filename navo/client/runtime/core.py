from __future__ import annotations

import asyncio
import logging

from typing import Any, Callable, Dict, List, Optional

from navo.util.config import SDKConfig, EnvManager
from navo.util.container import Container
from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Attachment, BootstrapData, Conversation, FriendRequest,
    Friendship, Message, User,
)
from navo.util.types.protocols import TokenStore
from navo.util.exceptions import AuthError, NavoError
from navo.util.transport import FileUploader, HTTPTransport, WebSocketTransport, setup_logging
from navo.captcha import solve_captcha_sync, asolve_captcha
from navo.admin import NavoAdmin

_logger = logging.getLogger("navo")


class NavoCoreMixin:
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

