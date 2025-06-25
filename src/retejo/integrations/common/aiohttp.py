import urllib.parse
from collections.abc import Mapping
from json import JSONDecodeError
from typing import Any, override

from aiohttp import ClientError, ClientSession, FormData

from retejo.errors import ClientLibraryError, MalformedResponseError
from retejo.integrations.common.base import AsyncBaseClient
from retejo.interfaces import Request, Response


class AiohttpBaseClient(AsyncBaseClient[Any]):
    _session: ClientSession

    def __init__(
        self,
        base_url: str,
        session: ClientSession | None = None,
        cookies: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__()
        self._base_url = base_url

        if session is None:
            self._session = ClientSession()
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
        if request.files is not None:
            data = FormData({})
            for name, file in request.files.items():
                data.add_field(
                    name,
                    filename=file.filename,
                    content_type=file.content_type,
                    value=file.contents,
                )
        else:
            data = None

        async with self._session.request(
            method=request.http_method,
            url=urllib.parse.urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            headers=request.headers,
            data=data,
        ) as response:
            try:
                response_json = await response.json()
            except ClientError as e:
                raise ClientLibraryError from e
            except JSONDecodeError as e:
                raise MalformedResponseError from e

            return Response(
                data=response_json,
                status_code=response.status,
            )

    @override
    async def close(self) -> None:
        await self._session.close()
