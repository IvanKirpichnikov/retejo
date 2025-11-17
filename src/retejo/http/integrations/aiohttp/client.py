from json import JSONDecodeError
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientError, ClientResponse, ClientSession, FormData
from typing_extensions import Self, override

from retejo.entities.file_obj import FileObj
from retejo.error import IntegrationError
from retejo.http.clients import BaseAsyncHttpClient
from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.errors import MalformedResponseError
from retejo.http.integrations.aiohttp.method_caller_factory import AiohttpMethodCallerFactory
from retejo.http.types import HttpMethodDumperType, HttpMethodResultLoaderType
from retejo.interfaces.method_caller import AsyncMethodCaller
from retejo.interfaces.method_caller_factory import MethodCallerFactory
from retejo.logger import Logger


class AiohttpClient(BaseAsyncHttpClient[ClientResponse]):
    __slots__ = ("_base_url", "_session")

    def __init__(
        self,
        base_url: str = "",
        method_dumper: HttpMethodDumperType | None = None,
        method_result_loader: HttpMethodResultLoaderType[ClientResponse] | None = None,
        logger: Logger | None = None,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            method_dumper=method_dumper,
            method_result_loader=method_result_loader,
            logger=logger,
        )

        self._base_url = base_url

        if session is None:
            session = ClientSession()

        self._session = session

    @override
    def get_method_caller_factory(
        self,
    ) -> MethodCallerFactory[
        Self,
        HttpMethod[Any],
        AsyncMethodCaller[Any, Any],
    ]:
        return AiohttpMethodCallerFactory(
            method_dumper=self._method_dumper,
            method_result_loader=self._method_result_loader,
        )

    @override
    async def send_request(
        self,
        request: HttpRequest,
    ) -> HttpResponse[ClientResponse]:
        if request.form is None:
            form_data = None
        else:
            form_data = FormData()
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

        async with self._session.request(
            method=request.http_method,
            url=urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            headers=request.headers,
            data=form_data,
        ) as response:
            response_data = await self.retrieve_response_body(response)
            return HttpResponse(
                raw_response=response,
                body=response_data,
                cookies=response.cookies,
                headers=response.headers,
                status_code=response.status,
            )

    @override
    async def retrieve_response_body(self, raw_response: ClientResponse) -> Any:
        try:
            return await raw_response.json()
        except ClientError as error:
            raise IntegrationError from error
        except JSONDecodeError as error:
            raise MalformedResponseError from error

    @override
    async def close(self) -> None:
        await self._session.close()
