from collections.abc import Mapping
from typing import Any, Protocol, override

from adaptix import Retort, as_sentinel, name_mapping

from retejo.errors import ClientError, ServerError
from retejo.interfaces.method import Method
from retejo.interfaces.request_conext_builder import RequestContextBuilder
from retejo.interfaces.session import Request, Response, Session
from retejo.markers import Omitted
from retejo.request_context_builder.builder import RequestContextBuilderImpl


class BaseSession(Session, Protocol):
    _body_retort: Retort
    _url_vars_retort: Retort
    _query_params_retort: Retort
    _response_retort: Retort
    _request_context_builder: RequestContextBuilder

    __slots__ = (
        "_body_retort",
        "_query_params_retort",
        "_request_context_builder",
        "_response_retort",
        "_url_vars_retort",
    )

    def __init__(self) -> None:
        self._body_retort = self._init_body_retort()
        self._url_vars_retort = self._init_url_vars_retort()
        self._query_params_retort = self._init_query_params_retort()
        self._response_retort = self._init_response_retort()
        self._request_context_builder = self._init_request_context_builder(
            body_retort=self._body_retort,
            url_vars_retort=self._url_vars_retort,
            query_params_retort=self._query_params_retort,
        )

    def _init_body_retort(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

    def _init_url_vars_retort(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

    def _init_query_params_retort(self) -> Retort:
        return Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

    def _init_response_retort(self) -> Retort:
        return Retort()

    def _init_request_context_builder(
        self,
        body_retort: Retort,
        url_vars_retort: Retort,
        query_params_retort: Retort,
    ) -> RequestContextBuilder:
        return RequestContextBuilderImpl(
            body_retort=body_retort,
            url_vars_retort=url_vars_retort,
            query_params_retort=query_params_retort,
        )

    @override
    def send_method[T](
        self,
        method: Method[T],
    ) -> T:
        request = self._make_request(method)
        response = self.send_request(request)

        self._handle_response(response)

        return self._load_response(
            tp=method.__returning__,
            data=response.body,
        )

    def _make_request(self, method: Method[Any]) -> Request:
        request_context = self._request_context_builder.build(method)

        if request_context.url_vars is None:
            url = method.__url__
        else:
            url = method.__url__.format_map(request_context.url_vars)

        return Request(
            url=url,
            body=request_context.body,
            headers=request_context.headers,
            http_method=method.__http_method__,
            query_params=request_context.query_params,
        )

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

    def _load_response[T](
        self,
        tp: type[T],
        data: Mapping[str, Any],
    ) -> T:
        return self._response_retort.load(data, tp)
