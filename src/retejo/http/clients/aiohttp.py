from collections.abc import Mapping
from json import JSONDecodeError
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientError, ClientResponse, ClientSession, FormData

from retejo.core.errors import IntegrationError
from retejo.http.clients.base import AsyncHttpClient
from retejo.http.entities import FileObj, HttpRequest, HttpResponse
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
        if request.form is not None:  # noqa: WPS504
            form_data = FormData({})
            for name, value in request.form.items():
                if isinstance(value, FileObj):
                    form_data.add_field(
                        name,
                        filename=value.filename,
                        content_type=value.content_type,
                        value=value.contents,
                    )
                else:
                    form_data.add_field(name, value)
        else:
            form_data = None

        async with self._session.request(
            method=request.http_method,
            url=urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            headers=request.headers,
            data=form_data,
        ) as response:
            response_data = await self.retrieve_response_data(response)

            return HttpResponse(
                raw=response,
                data=response_data,
                status_code=response.status,
            )

    async def retrieve_response_data(self, raw_response: ClientResponse) -> Any:
        try:
            return await raw_response.json()
        except ClientError as error:
            raise IntegrationError from error
        except JSONDecodeError as error:
            raise MalformedResponseError from error

    async def close(self) -> None:
        await self._session.close()
