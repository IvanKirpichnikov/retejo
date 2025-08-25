# flake8: noqa: WPS102
from abc import abstractmethod
from logging import DEBUG
from types import TracebackType
from typing import Any, Final, Generic, TypeVar

from typing_extensions import Self, override

from retejo.core.clients import AsyncClient
from retejo.http.clients.base import BaseHttpClient
from retejo.http.entities import HttpMethod, HttpRequest, HttpResponse
from retejo.http.errors import ClientError, ServerError

SERVER_ERROR_MIN_STATUS_CODE: Final = 500
CLIENT_ERROR_MIN_STATUS_CODE: Final = 400

_MethodResultT = TypeVar("_MethodResultT")
_RawResponseT = TypeVar("_RawResponseT")


class AsyncHttpClient(
    BaseHttpClient,
    AsyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawResponseT]],
    Generic[_RawResponseT],
):
    __slots__ = ()

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

    @override
    async def aclose(self) -> None:
        await self.close()

    @override
    async def send_method(
        self,
        method: HttpMethod[_MethodResultT],
    ) -> _MethodResultT:
        await self.handle_method(method)

        request = self.method_to_request(method)
        await self.handle_request(request)

        response = await self.send_request(request)
        await self.handle_response(response)

        return self.load_method_result(
            response=response,
            method_result=method.__result__,
        )

    @override
    async def handle_method(self, method: HttpMethod[_MethodResultT]) -> None:
        self._logger_state.method.log(
            DEBUG,
            "Called %r",
            method,
        )

    @abstractmethod
    async def retrieve_response_data(self, raw_response: _RawResponseT) -> Any:
        raise NotImplementedError

    @override
    async def handle_request(
        self,
        request: HttpRequest,
    ) -> None:
        self._logger_state.request.log(
            DEBUG,
            "Send %r",
            request,
        )

    @override
    async def handle_response(
        self,
        response: HttpResponse[_RawResponseT],
    ) -> None:
        self._logger_state.response.log(
            DEBUG,
            "Received %r",
            response,
        )

        if response.status_code >= CLIENT_ERROR_MIN_STATUS_CODE:
            await self.handle_error_response(response)

    @override
    async def handle_error_response(self, response: HttpResponse[_RawResponseT]) -> None:
        if CLIENT_ERROR_MIN_STATUS_CODE <= response.status_code < SERVER_ERROR_MIN_STATUS_CODE:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)
