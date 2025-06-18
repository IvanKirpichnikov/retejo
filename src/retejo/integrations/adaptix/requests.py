from collections.abc import Mapping
from typing import Any

from requests import Session

from retejo.integrations.adaptix.base import BaseAdaptixClient
from retejo.integrations.common.requests import RequestsBaseClient


class RequestsAdaptixClient(
    BaseAdaptixClient,
    RequestsBaseClient,
):
    def __init__(
        self,
        base_url: str,
        session: Session | None = None,
        cookies: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            session=session,
            cookies=cookies,
            headers=headers,
        )
