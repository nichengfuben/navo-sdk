from __future__ import annotations

from navo.ext import NavoApiMixin
from navo.client.runtime.core import NavoCoreMixin
from navo.client.runtime.events import NavoEventsMixin
from navo.client.runtime.health import NavoHealthMixin
from navo.client.login.auth import NavoAuthMixin
from navo.client.login.profile import NavoProfileMixin
from navo.client.login.bootstrap import NavoBootstrapMixin
from navo.client.chat.conversations import NavoConversationsMixin
from navo.client.chat.messages import NavoMessagesMixin
from navo.client.chat.members import NavoMembersMixin
from navo.client.chat.friends import NavoFriendsMixin
from navo.client.runtime.upload import NavoUploadMixin
from navo.client.runtime.wsops import NavoWsOpsMixin


class Navo(
    NavoCoreMixin,
    NavoEventsMixin,
    NavoAuthMixin,
    NavoProfileMixin,
    NavoBootstrapMixin,
    NavoConversationsMixin,
    NavoMessagesMixin,
    NavoMembersMixin,
    NavoFriendsMixin,
    NavoUploadMixin,
    NavoWsOpsMixin,
    NavoHealthMixin,
    NavoApiMixin,
):
    """Navo IM SDK 主客户端。"""


__all__ = ["Navo"]
