from json import JSONDecodeError
from typing import Any
from urllib.parse import urljoin

import httpx
from typing_extensions import override

from retejo.core.errors import IntegrationError
from retejo.http.clients.async_ import AsyncHttpClient
from retejo.http.entities import FileObj, HttpRequest, HttpResponse
from retejo.http.errors import MalformedResponseError
from retejo.http.logger_state import HttpLoggerState


class HttpxAsyncClient(AsyncHttpClient[httpx.Response]):
    __slots__ = ("_base_url", "_client")

    def __init__(
        self,
        base_url: str = "",
        client: httpx.AsyncClient | None = None,
        logger_state: HttpLoggerState | None = None,
    ) -> None:
        if logger_state is None:
            logger_state = HttpLoggerState()

        super().__init__(logger_state)

        self._base_url = base_url

        if client is None:
            self._client = httpx.AsyncClient()
        else:
            self._client = client

    @override
    async def send_request(
        self,
        request: HttpRequest,
    ) -> HttpResponse[httpx.Response]:
        if request.form is not None:  # noqa: WPS504
            files = {}
            data = {}
            for key, value in request.form.items():
                if isinstance(value, FileObj):
                    files[key] = (
                        value.filename or key,
                        value.contents,
                        value.content_type,
                    )
                else:
                    data[key] = value
        else:
            files = None
            data = None

        response = await self._client.request(
            method=request.http_method,
            url=urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            headers=request.headers,
            data=data,
            files=files,
        )
        response_data = await self.retrieve_response_data(response)

        return HttpResponse(
            data=response_data,
            headers=response.headers,
            cookies=response.cookies,
            status_code=response.status_code,
            raw=response,
        )

    @override
    async def retrieve_response_data(self, raw_response: httpx.Response) -> Any:
        try:
            return raw_response.json()
        except httpx.HTTPStatusError as error:
            raise IntegrationError from error
        except JSONDecodeError as error:
            raise MalformedResponseError from error

    @override
    async def close(self) -> None:
        await self._client.aclose()
