from abc import abstractmethod
from types import NoneType
from typing import Any, Generic, TypeVar

from adaptix import Omitted, Retort, as_is_dumper, as_sentinel

from retejo.core.clients import AsyncClient, SyncClient
from retejo.core.entities import RequestContextProxy
from retejo.http import loggers
from retejo.http.entities import FileObj, HttpMethod, HttpRequest, HttpResponse
from retejo.http.errors import ClientError, ServerError
from retejo.http.markers import BodyMarker, FileMarker, HeaderMarker, QueryParamMarker, UrlVarMarker
from retejo.utils._fixed_type_hint_tags_unwrapping_provider import FixedTypeHintTagsUnwrappingProvider
from retejo.utils.method_dumper import method_dumper

_MethodResultT = TypeVar("_MethodResultT")
_RawResponseT = TypeVar("_RawResponseT")


class BaseHttpClient:
    __slots__ = (
        "method_dumper",
        "response_loader",
    )

    def __init__(self) -> None:
        self.method_dumper = self.init_method_dumper()
        self.response_loader = self.init_response_loader()

    def init_method_dumper(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                as_is_dumper(FileObj),
                method_dumper(),
                FixedTypeHintTagsUnwrappingProvider(),
            ]
        )

    def init_response_loader(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                FixedTypeHintTagsUnwrappingProvider(),
            ]
        )

    def method_to_request(self, method: HttpMethod[Any]) -> HttpRequest:
        request_context = RequestContextProxy(self.method_dumper.dump(method))

        url_vars = request_context.get(UrlVarMarker)
        if url_vars is None:  # noqa: SIM108
            url = method.__url__
        else:
            url = method.__url__.format_map(url_vars)

        return HttpRequest(
            url=url,
            http_method=method.__http_method__,
            body=request_context.get(BodyMarker),
            headers=request_context.get(HeaderMarker),
            query_params=request_context.get(QueryParamMarker),
            files=request_context.get(FileMarker),
            context=request_context,
        )

    def load_method_result(
        self,
        response: HttpResponse[_RawResponseT],
        method_result: type[_MethodResultT],
    ) -> _MethodResultT:
        if method_result in (NoneType, None):
            return None  # type: ignore[return-value]

        return self.response_loader.load(response.data, method_result)



class SyncHttpClient(
    BaseHttpClient,
    SyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawResponseT]],
    Generic[_RawResponseT],
):
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
            response=response,
            method_result=method.__result__,
        )

    def handle_method(self, method: HttpMethod[_MethodResultT]) -> None:
        loggers.method.debug("Called %r", method)

    @abstractmethod
    def retrieve_response_data(self, raw_response: _RawResponseT) -> Any:
        raise NotImplementedError

    def handle_request(
        self,
        request: HttpRequest,
    ) -> None:
        loggers.request.debug("Send %r", request)

    def handle_response(
        self,
        response: HttpResponse[_RawResponseT],
    ) -> None:
        loggers.response.debug("Received %r", response)

        if response.status_code >= 400:
            self.handle_error_response(response)

    def handle_error_response(self, response: HttpResponse[_RawResponseT]) -> None:
        if 400 <= response.status_code < 500:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)



class AsyncHttpClient(
    BaseHttpClient,
    AsyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawResponseT]],
    Generic[_RawResponseT],
):
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

    async def handle_method(self, method: HttpMethod[_MethodResultT]) -> None:
        loggers.method.debug("Called %s", method)

    @abstractmethod
    async def retrieve_response_data(self, raw_response: _RawResponseT) -> Any:
        raise NotImplementedError

    async def handle_request(
        self,
        request: HttpRequest,
    ) -> None:
        loggers.request.debug("Send %s", request)

    async def handle_response(
        self,
        response: HttpResponse[_RawResponseT],
    ) -> None:
        loggers.response.debug("Received %s", response)

        if response.status_code >= 400:
            await self.handle_error_response(response)

    async def handle_error_response(self, response: HttpResponse[_RawResponseT]) -> None:
        if 400 <= response.status_code < 500:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)
