import urllib.parse
from collections.abc import Mapping
from json import JSONDecodeError
from typing import Any

from aiohttp import ClientError, ClientResponse, ClientSession, FormData

from retejo.core.errors import IntegrationError
from retejo.http.clients.base import AsyncHttpClient
from retejo.http.entities import HttpRequest, HttpResponse
from retejo.http.errors import MalformedResponseError


class AiohttpClient(AsyncHttpClient[ClientResponse]):
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

    async def send_request(
        self,
        request: HttpRequest,
    ) -> HttpResponse[ClientResponse]:
        if request.files is not None:
            form_data = FormData({})
            for name, file in request.files.items():
                form_data.add_field(
                    name,
                    filename=file.filename,
                    content_type=file.content_type,
                    value=file.contents,
                )
        else:
            form_data = None

        async with self._session.request(
            method=request.http_method,
            url=urllib.parse.urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            headers=request.headers,
            data=form_data,
        ) as response:
            data = await self.retrieve_response_data(response)

            return HttpResponse(
                raw=response,
                data=data,
                status_code=response.status,
            )

    async def retrieve_response_data(self, raw_response: ClientResponse) -> Any:
        try:
            return await raw_response.json()
        except ClientError as e:
            raise IntegrationError from e
        except JSONDecodeError as e:
            raise MalformedResponseError from e

    async def close(self) -> None:
        await self._session.close()
