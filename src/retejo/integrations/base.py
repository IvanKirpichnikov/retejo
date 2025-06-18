from collections.abc import Mapping, MutableMapping
from types import NoneType
from typing import Any, override

from adaptix import Retort, as_sentinel, name_mapping

from retejo.errors import ClientError, ServerError
from retejo.interfaces import (
    AsyncClient,
    Factory,
    Request,
    RequestContextBuilder,
    Response,
    SyncClient,
)
from retejo.markers import (
    BaseMarker,
    BodyMarker,
    HeaderMarker,
    Omitted,
    QueryParamMarker,
    UrlVarMarker,
)
from retejo.method import Method
from retejo.request_context_builder import SimpleRequestContextBuilder

type MarkersFactorties = MutableMapping[type[BaseMarker], Factory]


class BaseClient:
    _response_factory: Factory
    _request_context_builder: RequestContextBuilder
    _markers_factories: MarkersFactorties

    __slots__ = (
        "_markers_factories",
        "_request_context_builder",
        "_response_factory",
    )

    def __init__(self) -> None:
        self._markers_factories = self.init_markers_factories()
        self._response_factory = self.init_response_factory()
        self._request_context_builder = self.init_request_context_builder()

    def init_markers_factories(self) -> MarkersFactorties:
        retort = Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

        return {
            BodyMarker: retort,
            UrlVarMarker: retort,
            HeaderMarker: retort,
            QueryParamMarker: retort,
        }

    def init_response_factory(self) -> Factory:
        return Retort()

    def init_request_context_builder(self) -> RequestContextBuilder:
        return SimpleRequestContextBuilder(self._markers_factories)

    def _method_to_request(self, method: Method[Any]) -> Request:
        request_context = self._request_context_builder.build(method)

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
            context=request_context,
        )

    def _load_method_returning[T](
        self,
        response: Mapping[str, Any],
        method_returning_tp: type[T],
    ) -> T:
        if method_returning_tp is NoneType:
            return None  # type: ignore[return-value]

        return self._response_factory.load(response, method_returning_tp)


class SyncBaseClient(BaseClient, SyncClient):
    @override
    def _handle_response(self, response: Response) -> None:
        if response.status_code >= 400:
            self._handle_error_response(response)

    @override
    def _handle_error_response(self, response: Response) -> None:
        if 400 <= response.status_code < 500:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)

    @override
    def send_method[T](
        self,
        method: Method[T],
    ) -> T:
        request = self._method_to_request(method)
        response = self.send_request(request)

        self._handle_response(response)

        return self._load_method_returning(
            response=response.data,
            method_returning_tp=method.__returning__,
        )


class AsyncBaseClient(BaseClient, AsyncClient):
    @override
    async def _handle_response(self, response: Response) -> None:
        if response.status_code >= 400:
            await self._handle_error_response(response)

    @override
    async def _handle_error_response(self, response: Response) -> None:
        if 400 <= response.status_code < 500:
            raise ClientError(response.status_code)
        else:
            raise ServerError(response.status_code)

    @override
    async def send_method[T](
        self,
        method: Method[T],
    ) -> T:
        request = self._method_to_request(method)
        response = await self.send_request(request)

        await self._handle_response(response)

        return self._load_method_returning(
            response=response.data,
            method_returning_tp=method.__returning__,
        )
