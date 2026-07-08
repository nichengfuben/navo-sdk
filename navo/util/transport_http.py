from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import aiohttp
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from navo.util.config import SDKConfig
from navo.util.exceptions import AuthError, NavoError, NetworkError
from navo.util.protocols import TokenStore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_logger = logging.getLogger("navo")


class HTTPTransport:
    """HTTP 传输层。封装同步/异步请求、令牌注入、重试。"""

    def __init__(
        self,
        config: SDKConfig,
        token_store: Optional[TokenStore] = None,
    ) -> None:
        self._config = config
        self._token_store = token_store
        self._session: Optional[requests.Session] = None
        self._async_session: Optional[aiohttp.ClientSession] = None

    @property
    def session(self) -> requests.Session:
        """同步 HTTP 会话（懒加载）。"""
        if self._session is None:
            self._session = self._create_sync_session()
        return self._session

    def _create_sync_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=self._config.max_retries,
            status_forcelist=self._config.retry_status_forcelist,
            backoff_factor=self._config.retry_backoff_factor,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    async def _get_async_session(self) -> aiohttp.ClientSession:
        if self._async_session is None or self._async_session.closed:
            self._async_session = aiohttp.ClientSession()
        return self._async_session

    def _build_headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "User-Agent": self._config.user_agent,
            "Accept": "application/json",
        }
        if self._token_store:
            token = self._token_store.get_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
        if extra:
            headers.update(extra)
        return headers

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        base = self._config.base_url.rstrip("/")
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{base}{path}"

    def _handle_response(self, resp: requests.Response) -> Any:
        if resp.status_code == 401:
            raise AuthError("未授权：令牌无效或已过期")
        if resp.status_code >= 400:
            try:
                data = resp.json()
                error_msg = data.get("error", resp.text)
            except Exception:
                error_msg = resp.text
            raise NavoError(f"HTTP {resp.status_code}: {error_msg}", code=resp.status_code)
        if resp.status_code == 204:
            return None
        return resp.json()

    # ==================================================================
    # 同步 API
    # ==================================================================

    def request(
        self,
        method: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """同步 HTTP 请求。"""
        url = self._build_url(path)
        merged_headers = self._build_headers(headers)
        try:
            resp = self.session.request(
                method,
                url,
                json=json_data,
                params=params,
                headers=merged_headers,
                timeout=self._config.timeout,
                verify=self._config.ssl_verify,
            )
            return self._handle_response(resp)
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(f"连接失败: {exc}") from exc
        except requests.exceptions.Timeout as exc:
            raise NavoError(f"请求超时: {exc}") from exc

    def upload_file_sync(
        self,
        path: str,
        file_path: str,
        field_name: str = "file",
        extra_fields: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """同步文件上传。"""
        url = self._build_url(path)
        merged_headers = self._build_headers()
        # 上传时不设置 Content-Type，让 requests 自动处理 multipart
        merged_headers.pop("Content-Type", None)
        merged_headers.pop("Accept", None)
        try:
            with open(file_path, "rb") as f:
                resp = self.session.post(
                    url,
                    files={field_name: f},
                    data=extra_fields or None,
                    headers=merged_headers,
                    timeout=self._config.timeout * 3,
                    verify=self._config.ssl_verify,
                )
            return self._handle_response(resp)
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(f"连接失败: {exc}") from exc
        except requests.exceptions.Timeout as exc:
            raise NavoError(f"上传超时: {exc}") from exc

    # ==================================================================
    # 异步 API
    # ==================================================================

    async def arequest(
        self,
        method: str,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """异步 HTTP 请求。"""
        url = self._build_url(path)
        merged_headers = self._build_headers(headers)
        session = await self._get_async_session()
        timeout = aiohttp.ClientTimeout(total=self._config.timeout)
        try:
            async with session.request(
                method,
                url,
                json=json_data,
                params=params,
                headers=merged_headers,
                timeout=timeout,
                ssl=self._config.ssl_verify,
            ) as resp:
                if resp.status == 401:
                    raise AuthError("未授权：令牌无效或已过期")
                if resp.status >= 400:
                    try:
                        data = await resp.json()
                        error_msg = data.get("error", await resp.text())
                    except Exception:
                        error_msg = await resp.text()
                    raise NavoError(f"HTTP {resp.status}: {error_msg}", code=resp.status)
                if resp.status == 204:
                    return None
                return await resp.json()
        except aiohttp.ClientConnectionError as exc:
            raise NetworkError(f"连接失败: {exc}") from exc
        except asyncio.TimeoutError as exc:
            raise NavoError(f"请求超时: {exc}") from exc

    async def upload_file_async(
        self,
        path: str,
        file_path: str,
        field_name: str = "file",
        extra_fields: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """异步文件上传。"""
        url = self._build_url(path)
        merged_headers = self._build_headers()
        merged_headers.pop("Content-Type", None)
        merged_headers.pop("Accept", None)
        session = await self._get_async_session()
        timeout = aiohttp.ClientTimeout(total=self._config.timeout * 3)
        try:
            data = aiohttp.FormData()
            if extra_fields:
                for key, value in extra_fields.items():
                    if value is not None:
                        data.add_field(key, str(value))
            filename = file_path.split("/")[-1].split("\\")[-1]
            with open(file_path, "rb") as f:
                data.add_field(field_name, f, filename=filename)
                async with session.post(
                    url, data=data, headers=merged_headers, timeout=timeout, ssl=self._config.ssl_verify,
                ) as resp:
                    if resp.status == 401:
                        raise AuthError("未授权")
                    if resp.status >= 400:
                        error_msg = await resp.text()
                        raise NavoError(f"HTTP {resp.status}: {error_msg}", code=resp.status)
                    return await resp.json()
        except aiohttp.ClientConnectionError as exc:
            raise NetworkError(f"连接失败: {exc}") from exc

    # ==================================================================
    # 资源释放
    # ==================================================================

    def close(self) -> None:
        """关闭同步会话。"""
        if self._session is not None:
            self._session.close()
            self._session = None

    async def aclose(self) -> None:
        """关闭异步会话。"""
        if self._async_session is not None and not self._async_session.closed:
            await self._async_session.close()
            self._async_session = None
        self.close()  # also close sync requests.Session


__all__ = ["HTTPTransport"]
