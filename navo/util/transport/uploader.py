from __future__ import annotations

from typing import Any, Dict, Optional

from navo.util.domain.models import Attachment
from navo.util.transport.http import HTTPTransport


class FileUploader:
    """文件上传器。"""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def upload(
        self,
        file_path: str,
        poster: Optional[str] = None,
        e2ee_conversation_id: Optional[str] = None,
    ) -> Attachment:
        extra: Dict[str, Any] = {}
        if poster is not None:
            extra["poster"] = poster
        if e2ee_conversation_id is not None:
            extra["e2eeConversationId"] = e2ee_conversation_id
        data = self._http.upload_file_sync(
            "/api/upload", file_path, extra_fields=extra or None,
        )
        return Attachment.from_dict(data)

    async def aupload(
        self,
        file_path: str,
        poster: Optional[str] = None,
        e2ee_conversation_id: Optional[str] = None,
    ) -> Attachment:
        extra: Dict[str, Any] = {}
        if poster is not None:
            extra["poster"] = poster
        if e2ee_conversation_id is not None:
            extra["e2eeConversationId"] = e2ee_conversation_id
        data = await self._http.upload_file_async(
            "/api/upload", file_path, extra_fields=extra or None,
        )
        return Attachment.from_dict(data)

    def check_nsfw(self, file_path: str) -> Dict[str, Any]:
        return self._http.upload_file_sync("/api/nsfw/check", file_path)

    async def acheck_nsfw(self, file_path: str) -> Dict[str, Any]:
        return await self._http.upload_file_async("/api/nsfw/check", file_path)


__all__ = ["FileUploader"]
