from __future__ import annotations

from typing import Any, Dict, List, Optional

from navo.util.decorators import async_require_login, require_login


def _body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class AdminSettingsMixin:
    # ======================================================================
    # Settings & configs
    # ======================================================================

    @require_login
    def get_settings(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/settings")

    @async_require_login
    async def aget_settings(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/settings")

    @require_login
    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/settings", json_data=settings)

    @async_require_login
    async def aupdate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/settings", json_data=settings)

    @require_login
    def get_captcha_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/captcha-config")

    @async_require_login
    async def aget_captcha_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/captcha-config")

    @require_login
    def update_captcha_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/captcha-config", json_data=config)

    @async_require_login
    async def aupdate_captcha_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/captcha-config", json_data=config)

    @require_login
    def get_ai_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/ai-config")

    @async_require_login
    async def aget_ai_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/ai-config")

    @require_login
    def update_ai_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/ai-config", json_data=config)

    @async_require_login
    async def aupdate_ai_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/ai-config", json_data=config)

    @require_login
    def test_ai(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/ai-test", json_data=config)

    @async_require_login
    async def atest_ai(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/ai-test", json_data=config)

    @require_login
    def get_ice_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/ice-config")

    @async_require_login
    async def aget_ice_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/ice-config")

    @require_login
    def update_ice_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/ice-config", json_data=config)

    @async_require_login
    async def aupdate_ice_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/ice-config", json_data=config)

    @require_login
    def get_translation_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/translation-config")

    @async_require_login
    async def aget_translation_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/translation-config")

    @require_login
    def update_translation_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/translation-config", json_data=config)

    @async_require_login
    async def aupdate_translation_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/translation-config", json_data=config)

    @require_login
    def get_getui_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/getui-config")

    @async_require_login
    async def aget_getui_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/getui-config")

    @require_login
    def update_getui_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/getui-config", json_data=config)

    @async_require_login
    async def aupdate_getui_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/getui-config", json_data=config)

    @require_login
    def test_getui(self) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/getui-test")

    @async_require_login
    async def atest_getui(self) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/getui-test")

    @require_login
    def list_push_tokens(self) -> List[Dict[str, Any]]:
        return self._http.request("GET", "/api/admin/push-tokens")

    @async_require_login
    async def alist_push_tokens(self) -> List[Dict[str, Any]]:
        return await self._http.arequest("GET", "/api/admin/push-tokens")

    @require_login
    def get_sms_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/sms-config")

    @async_require_login
    async def aget_sms_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/sms-config")

    @require_login
    def update_sms_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/sms-config", json_data=config)

    @async_require_login
    async def aupdate_sms_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/sms-config", json_data=config)

    @require_login
    def test_sms(self, phone: str) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/sms-test", json_data={"phone": phone})

    @async_require_login
    async def atest_sms(self, phone: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/sms-test", json_data={"phone": phone})

    @require_login
    def get_email_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/email-config")

    @async_require_login
    async def aget_email_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/email-config")

    @require_login
    def update_email_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/email-config", json_data=config)

    @async_require_login
    async def aupdate_email_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/email-config", json_data=config)

    @require_login
    def test_email(self, email: str) -> Dict[str, Any]:
        return self._http.request("POST", "/api/admin/email-test", json_data={"email": email})

    @async_require_login
    async def atest_email(self, email: str) -> Dict[str, Any]:
        return await self._http.arequest("POST", "/api/admin/email-test", json_data={"email": email})

    @require_login
    def get_nsfw_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/nsfw-config")

    @async_require_login
    async def aget_nsfw_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/nsfw-config")

    @require_login
    def update_nsfw_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/nsfw-config", json_data=config)

    @async_require_login
    async def aupdate_nsfw_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/nsfw-config", json_data=config)

    @require_login
    def get_sso_config(self) -> Dict[str, Any]:
        return self._http.request("GET", "/api/admin/sso-config")

    @async_require_login
    async def aget_sso_config(self) -> Dict[str, Any]:
        return await self._http.arequest("GET", "/api/admin/sso-config")

    @require_login
    def update_sso_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", "/api/admin/sso-config", json_data=config)

    @async_require_login
    async def aupdate_sso_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._http.arequest("PUT", "/api/admin/sso-config", json_data=config)

