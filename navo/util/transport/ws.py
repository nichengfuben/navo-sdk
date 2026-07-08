from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable, Dict, Optional

import websockets
import websockets.exceptions

from navo.util.config import SDKConfig
from navo.util.transport.events import EventEmitter

_logger = logging.getLogger("navo")


class WebSocketTransport(EventEmitter):
    """WebSocket 传输层。自动重连 + 心跳 + 事件分发。"""

    def __init__(self, config: SDKConfig) -> None:
        super().__init__()
        self._config = config
        self._ws = None
        self._running = False
        self._listen_task: Optional[asyncio.Task[None]] = None
        self._reconnect_count = 0

    @property
    def connected(self) -> bool:
        if self._ws is None:
            return False
        try:
            state = self._ws.state
            # websockets v13+ uses State enum
            return state.name == "OPEN"
        except AttributeError:
            # Fallback for older versions
            try:
                return self._ws.open
            except AttributeError:
                return False

    async def start(self, auth_token: str) -> None:
        """连接并认证。"""
        self._running = True
        await self._connect(auth_token)

    async def _connect(self, auth_token: str) -> None:
        """建立连接并发送认证。"""
        try:
            ssl_param: Any = None
            if self._config.ws_url.startswith("wss://"):
                import ssl as _ssl
                if not self._config.ssl_verify:
                    ssl_param = _ssl.create_default_context()
                    ssl_param.check_hostname = False
                    ssl_param.verify_mode = _ssl.CERT_NONE
                else:
                    try:
                        import certifi
                        ssl_param = _ssl.create_default_context(cafile=certifi.where())
                    except ImportError:
                        ssl_param = _ssl.create_default_context()
            connect_kwargs: Dict[str, Any] = {
                "ping_interval": self._config.ws_ping_interval,
                "ping_timeout": self._config.ws_ping_timeout,
                "max_size": 2 ** 22,
            }
            if ssl_param is not None:
                connect_kwargs["ssl"] = ssl_param
            self._ws = await websockets.connect(
                self._config.ws_url,
                **connect_kwargs,
            )
            # 发送认证
            await self._ws.send(json.dumps({"type": "auth", "token": auth_token}))
            self._reconnect_count = 0
            _logger.info("WebSocket 已连接: %s", self._config.ws_url)
        except Exception as exc:
            _logger.error("WebSocket 连接失败: %s", exc)
            if self._running and self._config.ws_auto_reconnect:
                await self._schedule_reconnect(auth_token)
            return

        # 启动监听循环
        self._listen_task = asyncio.create_task(self._listen_loop(auth_token))

    async def _listen_loop(self, auth_token: str) -> None:
        """持续监听消息。"""
        try:
            while self._running and self.connected:
                try:
                    raw = await self._ws.recv()
                except websockets.exceptions.ConnectionClosed:
                    _logger.info("WebSocket 连接已关闭")
                    break
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    _logger.warning("收到无效 JSON 消息")
                    continue
                event_type = event.get("type", "unknown")
                await self.emit(event_type, event)
                await self.emit("*", event)  # 通配事件
        except Exception as exc:
            _logger.error("WebSocket 监听异常: %s", exc)
        finally:
            if self._running and self._config.ws_auto_reconnect:
                await self._schedule_reconnect(auth_token)

    async def _schedule_reconnect(self, auth_token: str) -> None:
        """指数退避重连。"""
        delay = min(
            self._config.ws_reconnect_delay * (2 ** self._reconnect_count),
            self._config.ws_max_reconnect_delay,
        )
        self._reconnect_count += 1
        _logger.info("将在 %ss 后重连 (第 %s 次)", delay, self._reconnect_count)
        await asyncio.sleep(delay)
        if self._running:
            await self._connect(auth_token)

    async def send(self, data: Dict[str, Any]) -> None:
        """发送 JSON 消息。"""
        if not self.connected:
            _logger.warning("WebSocket 未连接，无法发送消息")
            return
        await self._ws.send(json.dumps(data))  # type: ignore[union-attr]

    async def stop(self) -> None:
        """关闭连接。"""
        self._running = False
        if self._listen_task and not self._listen_task.done():
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass
        self._ws = None


__all__ = ["WebSocketTransport"]
