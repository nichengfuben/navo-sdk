from __future__ import annotations

from typing import Any, Optional

from navo.util.types.models import User
from navo.ext.auth.system import ExtSystemMixin
from navo.ext.auth.auth import ExtAuthMixin
from navo.ext.auth.account import ExtAccountMixin
from navo.ext.chat.conversation import ExtConversationMixin
from navo.ext.chat.social import ExtSocialMixin
from navo.ext.chat.notify import ExtNotifyMixin
from navo.ext.extra.misc import ExtMiscMixin
from navo.ext.extra.wsext import ExtWsMixin


class NavoApiMixin(
    ExtSystemMixin,
    ExtAuthMixin,
    ExtAccountMixin,
    ExtConversationMixin,
    ExtSocialMixin,
    ExtNotifyMixin,
    ExtMiscMixin,
    ExtWsMixin,
):
    """Navo IM 扩展 API mixin 组合。"""

    _http: Any
    _ws: Any
    _config: Any
    _token_store: Any
    _me: Optional[User]
    _uploader: Any


__all__ = ["NavoApiMixin"]
