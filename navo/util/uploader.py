from __future__ import annotations

from navo.util.models import Attachment
from navo.util.transport_http import HTTPTransport


class FileUploader:
    """文件上传器。"""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def upload(self, file_path: str) -> Attachment:
        data = self._http.upload_file_sync("/api/upload", file_path)
        return Attachment.from_dict(data)

    async def aupload(self, file_path: str) -> Attachment:
        data = await self._http.upload_file_async("/api/upload", file_path)
        return Attachment.from_dict(data)


__all__ = ["FileUploader"]
