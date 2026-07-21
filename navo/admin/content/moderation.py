from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminModerationMixin:
    # ======================================================================
    # Sensitive words
    # ======================================================================

    @require_login
    def list_sensitive_words(self, **kwargs: Any) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/sensitive-words", params=_body(
            page=kwargs.get("page"), pageSize=kwargs.get("page_size"),
            search=kwargs.get("search"), policy=kwargs.get("policy"),
        ))

    @async_require_login
    async def alist_sensitive_words(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/sensitive-words", params=_body(
            page=kwargs.get("page"), pageSize=kwargs.get("page_size"),
            search=kwargs.get("search"), policy=kwargs.get("policy"),
        ))

    @require_login
    def add_sensitive_words(self, words: List[str], policy: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/sensitive-words", json_data=_body(words=words, policy=policy))

    @async_require_login
    async def aadd_sensitive_words(self, words: List[str], policy: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/sensitive-words", json_data=_body(words=words, policy=policy))

    @require_login
    def delete_sensitive_words(self, ids: List[str]) -> Dict[str, Any]:
        return self._http.request("DELETE", "/api/admin/sensitive-words", json_data={"ids": ids})

    @async_require_login
    async def adelete_sensitive_words(self, ids: List[str]) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", "/api/admin/sensitive-words", json_data={"ids": ids})

    # ======================================================================
    # Sticker packs (admin)
    # ======================================================================

    @require_login
    def create_sticker_pack(self, name: str) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/sticker-packs", json_data={"name": name})

    @async_require_login
    async def acreate_sticker_pack(self, name: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/sticker-packs", json_data={"name": name})

    @require_login
    def update_sticker_pack(self, pack_id: str, name: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"/api/admin/sticker-packs/{pack_id}", json_data={"name": name})

    @async_require_login
    async def aupdate_sticker_pack(self, pack_id: str, name: str) -> Dict[str, Any]:
        return await self._http.arequest("PATCH", f"/api/admin/sticker-packs/{pack_id}", json_data={"name": name})

    @require_login
    def delete_sticker_pack(self, pack_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/sticker-packs/{pack_id}")

    @async_require_login
    async def adelete_sticker_pack(self, pack_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/sticker-packs/{pack_id}")

    @require_login
    def add_sticker(self, pack_id: str, name: str, file_url: str, mime_type: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", f"/api/admin/sticker-packs/{pack_id}/stickers", json_data=_body(
            name=name, fileUrl=file_url, mimeType=mime_type,
        ))

    @async_require_login
    async def aadd_sticker(self, pack_id: str, name: str, file_url: str, mime_type: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", f"/api/admin/sticker-packs/{pack_id}/stickers", json_data=_body(
            name=name, fileUrl=file_url, mimeType=mime_type,
        ))

    @require_login
    def update_sticker(self, pack_id: str, sticker_id: str, name: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}", json_data={"name": name})

    @async_require_login
    async def aupdate_sticker(self, pack_id: str, sticker_id: str, name: str) -> Dict[str, Any]:
        return await self._http.arequest("PATCH", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}", json_data={"name": name})

    @require_login
    def delete_sticker(self, pack_id: str, sticker_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}")

    @async_require_login
    async def adelete_sticker(self, pack_id: str, sticker_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/sticker-packs/{pack_id}/stickers/{sticker_id}")

    # ======================================================================
    # Whitelists
    # ======================================================================

    @require_login
    def list_email_whitelist(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/email-whitelist")

    @async_require_login
    async def alist_email_whitelist(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/email-whitelist")

    @require_login
    def add_email_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/email-whitelist", json_data=_body(pattern=pattern, note=note))

    @async_require_login
    async def aadd_email_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/email-whitelist", json_data=_body(pattern=pattern, note=note))

    @require_login
    def delete_email_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/email-whitelist/{entry_id}")

    @async_require_login
    async def adelete_email_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/email-whitelist/{entry_id}")

    @require_login
    def list_phone_whitelist(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/phone-whitelist")

    @async_require_login
    async def alist_phone_whitelist(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/phone-whitelist")

    @require_login
    def add_phone_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/phone-whitelist", json_data=_body(pattern=pattern, note=note))

    @async_require_login
    async def aadd_phone_whitelist(self, pattern: str, note: Optional[str] = None) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/phone-whitelist", json_data=_body(pattern=pattern, note=note))

    @require_login
    def delete_phone_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"/api/admin/phone-whitelist/{entry_id}")

    @async_require_login
    async def adelete_phone_whitelist(self, entry_id: str) -> Dict[str, Any]:
        return await self._http.arequest("DELETE", f"/api/admin/phone-whitelist/{entry_id}")


__all__ = ["NavoAdmin"]
