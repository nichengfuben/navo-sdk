from __future__ import annotations

from typing import TYPE_CHECKING

from navo.admin.users.base import AdminBaseMixin
from navo.admin.users.users import AdminUsersMixin
from navo.admin.content.channels import AdminChannelsMixin
from navo.admin.content.messages import AdminMessagesMixin
from navo.admin.content.moderation import AdminModerationMixin
from navo.admin.platform.settings import AdminSettingsMixin
from navo.admin.platform.notify import AdminNotifyMixin
from navo.admin.platform.org import AdminOrgMixin

if TYPE_CHECKING:
    from navo.client import Navo


class NavoAdmin(
    AdminBaseMixin,
    AdminUsersMixin,
    AdminChannelsMixin,
    AdminMessagesMixin,
    AdminSettingsMixin,
    AdminNotifyMixin,
    AdminOrgMixin,
    AdminModerationMixin,
):
    """Navo IM 管理后台 API 客户端。"""

    def __init__(self, client: "Navo") -> None:
        self._client = client

    @property
    def _token_store(self):
        return self._client.token_store

    @property
    def _http(self):
        return self._client.http


__all__ = ["NavoAdmin"]
