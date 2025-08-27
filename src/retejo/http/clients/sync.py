from abc import abstractmethod
from logging import DEBUG
from types import TracebackType
from typing import Any, Final, Generic, TypeVar

from typing_extensions import Self, override

from retejo.core.clients import SyncClient
from retejo.http.clients.base import BaseHttpClient
from retejo.http.entities import HttpMethod, HttpRequest, HttpResponse
from retejo.http.errors import ClientError, ServerError

SERVER_ERROR_MIN_STATUS_CODE: Final = 500
CLIENT_ERROR_MIN_STATUS_CODE: Final = 400

_MethodResultT = TypeVar("_MethodResultT")
_RawResponseT = TypeVar("_RawResponseT")


class SyncHttpClient(
    BaseHttpClient,
    SyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawResponseT]],
    Generic[_RawResponseT],
):
    __slots__ = ()

    @override
    def __enter__(self) -> Self:
        return self

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    @override
    def send_method(
        self,
        method: HttpMethod[_MethodResultT],
    ) -> _MethodResultT:
        self.handle_method(method)

        request = self.method_to_request(method)
        self.handle_request(request)

        response = self.send_request(request)
        self.handle_response(response)

        return self.load_method_result(
            request=request,
            response=response,
            method_result=method.__result__,
        )

    @override
    def handle_method(self, method: HttpMethod[_MethodResultT]) -> None:
        self._logger_state.method.log(
            DEBUG,
            "Called %r",
            method,
        )

    @abstractmethod
    def retrieve_response_data(self, raw_response: _RawResponseT) -> Any:
        raise NotImplementedError

    @override
    def handle_request(
        self,
        request: HttpRequest,
    ) -> None:
        self._logger_state.request.log(
            DEBUG,
            "Send %r",
            request,
        )

    @override
    def handle_response(
        self,
        response: HttpResponse[_RawResponseT],
    ) -> None:
        self._logger_state.response.log(
            DEBUG,
            "Received %r",
            response,
        )

        if response.status_code >= CLIENT_ERROR_MIN_STATUS_CODE:
            self.handle_error_response(response)

    @override
    def handle_error_response(self, response: HttpResponse[_RawResponseT]) -> None:
        if CLIENT_ERROR_MIN_STATUS_CODE <= response.status_code < SERVER_ERROR_MIN_STATUS_CODE:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)
