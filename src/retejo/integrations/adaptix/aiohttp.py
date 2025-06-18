from collections.abc import Mapping
from typing import Any

from aiohttp import ClientSession

from retejo.integrations.adaptix.base import BaseAdaptixClient
from retejo.integrations.common.aiohttp import AiohttpBaseClient


class AiohttpAdaptixClient(
    BaseAdaptixClient,
    AiohttpBaseClient,
):
    def __init__(
        self,
        base_url: str,
        session: ClientSession | None = None,
        cookies: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            session=session,
            cookies=cookies,
            headers=headers,
        )
