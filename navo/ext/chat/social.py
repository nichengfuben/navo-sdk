from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login
from navo.util.types.models import (
    Conversation, ForwardedMessage, Message, Notification,
    Organization, StickerPack, User,
)


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class ExtSocialMixin:
    # ======================================================================
    # 好友扩展
    # ======================================================================

    @require_login
    def set_friend_note(self, user_id: str, note: Optional[str] = None) -> bool:
        self._http.request("PATCH", f"/api/friends/{user_id}/note", json_data={"note": note})
        return True

    @async_require_login
    async def aset_friend_note(self, user_id: str, note: Optional[str] = None) -> bool:
        await self._http.arequest("PATCH", f"/api/friends/{user_id}/note", json_data={"note": note})
        return True

