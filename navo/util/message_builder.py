from __future__ import annotations

from typing import Any, Dict, Optional


class MessageBuilder:
    """消息构建器。辅助构造 send_message 的参数。"""

    def __init__(self, receiver_id: int) -> None:
        self._receiver_id = receiver_id
        self._content: str = ""
        self._msg_type: Optional[str] = None
        self._file_path: Optional[str] = None

    def content(self, text: str) -> "MessageBuilder":
        """设置文本内容。"""
        self._content = text
        return self

    def msg_type(self, msg_type: str) -> "MessageBuilder":
        """设置消息类型 (text/image/file)。"""
        self._msg_type = msg_type
        return self

    def file(self, file_path: str) -> "MessageBuilder":
        """设置文件路径。"""
        self._file_path = file_path
        return self

    def build(self) -> Dict[str, Any]:
        """构建 send_message 参数字典。"""
        result: Dict[str, Any] = {
            "receiver_id": self._receiver_id,
            "content": self._content,
        }
        if self._msg_type:
            result["msg_type"] = self._msg_type
        if self._file_path:
            result["file_path"] = self._file_path
        return result


__all__ = ["MessageBuilder"]
