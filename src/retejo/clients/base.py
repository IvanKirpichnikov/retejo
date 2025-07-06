from collections.abc import Mapping
from types import NoneType
from typing import Any, TypeVar

from adaptix import Retort, as_is_dumper, as_sentinel, bound

from retejo import loggers
from retejo.errors import ClientError, ServerError
from retejo.file_obj import FileObj
from retejo.interfaces import (
    AsyncClient,
    Request,
    Response,
    SyncClient,
)
from retejo.markers.body import BodyMarker
from retejo.markers.file import FileMarker
from retejo.markers.header import HeaderMarker
from retejo.markers.omitted import Omitted
from retejo.markers.query_param import QueryParamMarker
from retejo.markers.url_var import UrlVarMarker
from retejo.method import Method
from retejo.utils.method_dumper import MethodDumperProvider
from retejo.utils.predicates.with_parents import WithParentsPredicate
from retejo.utils.request_context_proxy import RequestContextProxy

T = TypeVar("T")


class BaseClient:
    __slots__ = (
        "_method_dumper",
        "_response_loader",
    )

    def __init__(self) -> None:
        self._method_dumper = self.init_method_dumper()
        self._response_loader = self.init_response_loader()

    def init_method_dumper(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                as_is_dumper(FileObj),
                bound(
                    WithParentsPredicate(Method),
                    MethodDumperProvider(),
                ),
            ]
        )

    def init_response_loader(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
            ]
        )

    def method_to_request(self, method: Method[Any]) -> Request:
        request_context = RequestContextProxy(self._method_dumper.dump(method))

        url_vars = request_context.get(UrlVarMarker)
        if url_vars is None:  # noqa: SIM108
            url = method.__url__
        else:
            url = method.__url__.format_map(url_vars)

        return Request(
            url=url,
            http_method=method.__method__,
            body=request_context.get(BodyMarker),
            headers=request_context.get(HeaderMarker),
            query_params=request_context.get(QueryParamMarker),
            files=request_context.get(FileMarker),
            context=request_context,
        )

    def load_method_returning(
        self,
        response: Mapping[str, Any],
        method_returning_tp: type[T],
    ) -> T:
        if method_returning_tp is NoneType:
            return None  # type: ignore[return-value]

        return self._response_loader.load(response, method_returning_tp)


class SyncBaseClient(BaseClient, SyncClient):
    def send_method(
        self,
        method: Method[T],
    ) -> T:
        self.do_method(method)

        request = self.method_to_request(method)
        self.do_request(request)

        response = self.send_request(request)
        self.do_response(response)

        return self.load_method_returning(
            response=response.data,
            method_returning_tp=method.__returning__,
        )

    def do_method(self, method: Method[T]) -> None:
        loggers.method.debug("Called %r", method)

    def do_request(
        self,
        request: Request,
    ) -> None:
        loggers.request.debug("Send %r", request)

    def do_response(
        self,
        response: Response,
    ) -> None:
        loggers.response.debug("Received %r", response)
        self.handle_response(response)

    def handle_response(self, response: Response) -> None:
        if response.status_code >= 400:
            self.handle_error_response(response)

    def handle_error_response(self, response: Response) -> None:
        if 400 <= response.status_code < 500:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)


class AsyncBaseClient(BaseClient, AsyncClient):
    async def send_method(
        self,
        method: Method[T],
    ) -> T:
        await self.do_method(method)

        request = self.method_to_request(method)
        await self.do_request(request)

        response = await self.send_request(request)
        await self.do_response(response)

        return self.load_method_returning(
            response=response.data,
            method_returning_tp=method.__returning__,
        )

    async def do_method(self, method: Method[T]) -> None:
        loggers.method.debug("Called %s", method)

    async def do_request(
        self,
        request: Request,
    ) -> None:
        loggers.request.debug("Send %s", request)

    async def do_response(
        self,
        response: Response,
    ) -> None:
        loggers.response.debug("Received %s", response)
        await self.handle_response(response)

    async def handle_response(self, response: Response) -> None:
        if response.status_code >= 400:
            await self.handle_error_response(response)

    async def handle_error_response(self, response: Response) -> None:
        if 400 <= response.status_code < 500:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)
