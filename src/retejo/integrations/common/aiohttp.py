from collections.abc import Mapping
from json import JSONDecodeError
from typing import Any, override

from aiohttp import ClientError, ClientSession

from retejo.errors import ClientLibraryError, MalformedResponseError
from retejo.integrations.common.base import AsyncBaseClient
from retejo.interfaces import Request, Response


class AiohttpBaseClient(AsyncBaseClient):
    _session: ClientSession

    def __init__(
        self,
        base_url: str,
        session: ClientSession | None = None,
        cookies: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__()

        if session is None:
            self._session = ClientSession(base_url)
        else:
            self._session = session

        if headers is not None:
            self._session.headers.update(headers)
        if cookies is not None:
            self._session.cookie_jar.update_cookies(cookies)

    @override
    async def send_request(
        self,
        request: Request,
    ) -> Response:
        async with self._session.request(
            method=request.http_method,
            url=request.url,
            params=request.query_params,
            json=request.body,
            headers=request.headers,
        ) as response:
            try:
                data = await response.json()
            except ClientError as e:
                raise ClientLibraryError from e
            except JSONDecodeError as e:
                raise MalformedResponseError from e

            return Response(
                data=data,
                status_code=response.status,
            )

    @override
    async def close(self) -> None:
        await self._session.close()
