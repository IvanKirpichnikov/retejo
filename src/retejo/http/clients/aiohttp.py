from json import JSONDecodeError
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientError, ClientResponse, ClientSession, FormData
from typing_extensions import override

from retejo.core.errors import IntegrationError
from retejo.http.clients.async_ import AsyncHttpClient
from retejo.http.entities import FileObj, HttpRequest, HttpResponse
from retejo.http.errors import MalformedResponseError
from retejo.http.logger_state import HttpLoggerState


class AiohttpClient(AsyncHttpClient[ClientResponse]):
    __slots__ = ("_base_url", "_session")

    def __init__(
        self,
        base_url: str = "",
        session: ClientSession | None = None,
        logger_state: HttpLoggerState | None = None,
    ) -> None:
        if logger_state is None:
            logger_state = HttpLoggerState()

        super().__init__(logger_state)

        self._base_url = base_url

        if session is None:
            self._session = ClientSession()
        else:
            self._session = session

    @override
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
                cookies=response.cookies,
                headers=response.headers,
                status_code=response.status,
            )

    @override
    async def retrieve_response_data(self, raw_response: ClientResponse) -> Any:
        try:
            return await raw_response.json()
        except ClientError as error:
            raise IntegrationError from error
        except JSONDecodeError as error:
            raise MalformedResponseError from error

    @override
    async def close(self) -> None:
        await self._session.close()
