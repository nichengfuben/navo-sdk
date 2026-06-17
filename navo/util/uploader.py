from __future__ import annotations

from typing import Any, Dict, Optional

from navo.util.transport_http import HTTPTransport


class FileUploader:
    """文件上传器。用于聊天文件和头像上传。"""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def upload_chat_file(self, file_path: str, receiver_id: int, content: str = "", msg_type: Optional[str] = None) -> Dict[str, Any]:
        """同步上传聊天文件。"""
        extra = {"receiverId": str(receiver_id), "content": content}
        if msg_type:
            extra["msgType"] = msg_type
        return self._http.upload_file_sync("/api/messages/send", file_path, field_name="file", extra_data=extra)

    async def aupload_chat_file(self, file_path: str, receiver_id: int, content: str = "", msg_type: Optional[str] = None) -> Dict[str, Any]:
        """异步上传聊天文件。"""
        extra = {"receiverId": str(receiver_id), "content": content}
        if msg_type:
            extra["msgType"] = msg_type
        return await self._http.upload_file_async("/api/messages/send", file_path, field_name="file", extra_data=extra)

    def upload_avatar(self, file_path: str) -> Dict[str, Any]:
        """同步上传头像。"""
        return self._http.upload_file_sync("/api/user/avatar", file_path, field_name="avatar")

    async def aupload_avatar(self, file_path: str) -> Dict[str, Any]:
        """异步上传头像。"""
        return await self._http.upload_file_async("/api/user/avatar", file_path, field_name="avatar")


__all__ = ["FileUploader"]
