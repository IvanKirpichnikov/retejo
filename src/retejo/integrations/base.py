from collections.abc import Mapping
from types import NoneType
from typing import Any, override

from adaptix import Retort, as_sentinel, name_mapping

from retejo.errors import ClientError, ServerError
from retejo.interfaces.client import AsyncClient, SyncClient
from retejo.interfaces.factory import Factory
from retejo.interfaces.method import Method
from retejo.interfaces.request_context_builder import RequestContextBuilder
from retejo.interfaces.sendable_request import Request, Response
from retejo.markers import Omitted
from retejo.request_context_builder import RequestContextBuilderImpl


class BaseClient:
    _request_body_factory: Factory
    _request_url_vars_factory: Factory
    _request_query_params_factory: Factory
    _response_factory: Factory
    _request_context_builder: RequestContextBuilder

    __slots__ = (
        "_request_body_factory",
        "_request_context_builder",
        "_request_query_params_factory",
        "_request_url_vars_factory",
        "_response_factory",
    )

    def __init__(self) -> None:
        self._request_body_factory = self._init_request_body_factory()
        self._request_url_vars_factory = self._init_request_url_vars_factory()
        self._request_query_params_factory = self._init_request_query_params_factory()
        self._response_factory = self._init_response_factory()
        self._request_context_builder = self._init_request_context_builder(
            body_factory=self._request_body_factory,
            url_vars_factory=self._request_url_vars_factory,
            query_params_factory=self._request_query_params_factory,
        )

    def _init_request_body_factory(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

    def _init_request_url_vars_factory(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

    def _init_request_query_params_factory(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

    def _init_response_factory(self) -> Retort:
        return Retort()

    def _init_request_context_builder(
        self,
        body_factory: Factory,
        url_vars_factory: Factory,
        query_params_factory: Factory,
    ) -> RequestContextBuilder:
        return RequestContextBuilderImpl(
            body_factory=body_factory,
            url_vars_factory=url_vars_factory,
            query_params_factory=query_params_factory,
        )

    def _method_to_request(self, method: Method[Any]) -> Request:
        request_context = self._request_context_builder.build(method)

        if request_context.url_vars is None:
            url = method.__url__
        else:
            url = method.__url__.format_map(request_context.url_vars)

        return Request(
            url=url,
            body=request_context.body,
            headers=request_context.headers,
            http_method=method.__method__,
            query_params=request_context.query_params,
        )

    def _load_response[T](
        self,
        tp: type[T],
        data: Mapping[str, Any],
    ) -> T:
        if tp is NoneType:
            return None  # type: ignore[return-value]

        return self._response_factory.load(data, tp)


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

        return self._load_response(
            tp=method.__returning__,
            data=response.body,
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

        return self._load_response(
            tp=method.__returning__,
            data=response.body,
        )
