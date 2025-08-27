from types import NoneType
from typing import Any, Final, TypeVar, cast

from adaptix import Retort

from retejo._internal.type_tools.basic_utils import is_subclass_soft
from retejo.core.entities import AnyResult, RequestContextProxy, SequenceResult
from retejo.core.factory import AdaptixFactory, Factory
from retejo.http.entities import HttpMethod, HttpRequest, HttpResponse, ResponseLoadData
from retejo.http.logger_state import HttpLoggerState
from retejo.http.markers import BodyMarker, FormMarker, HeaderMarker, QueryParamMarker, UrlVarMarker
from retejo.http.providers import http_method_dumper_provider, http_response_loader_provider

_NONE_TYPES: Final = (NoneType, None)

_RawResponseT = TypeVar("_RawResponseT")
_MethodResultT = TypeVar("_MethodResultT")


class BaseHttpClient:
    __slots__ = (
        "_logger_state",
        "_method_dumper",
        "_response_loader",
    )

    def __init__(
        self,
        logger_state: HttpLoggerState,
    ) -> None:
        self._method_dumper = self.init_method_dumper()
        self._response_loader = self.init_response_loader()
        self._logger_state = logger_state

    def init_method_dumper(self) -> Factory:
        retort = Retort(recipe=[http_method_dumper_provider()])
        return AdaptixFactory(retort)

    def init_response_loader(self) -> Factory:
        retort = Retort(recipe=[http_response_loader_provider()])
        return AdaptixFactory(retort)

    def method_to_request(self, method: HttpMethod[Any]) -> HttpRequest:
        request_context = RequestContextProxy(self._method_dumper.dump(method))

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
            form=request_context.get(FormMarker),
            context=request_context,
        )

    def load_method_result(
        self,
        request: HttpRequest,
        response: HttpResponse[_RawResponseT],
        method_result: type[_MethodResultT],
    ) -> _MethodResultT:
        if method_result in _NONE_TYPES:
            return cast("_MethodResultT", None)

        if is_subclass_soft(method_result, AnyResult):
            return cast("_MethodResultT", response.data)

        response_load_data = self._make_response_load_data(response)

        result = self._response_loader.load(
            response_load_data,
            method_result,
        )

        if isinstance(result, SequenceResult):
            return cast("_MethodResultT", result.result)
        return result

    def _make_response_load_data(self, response: HttpResponse[_RawResponseT]) -> ResponseLoadData:
        return {
            "data": response.data,
            "cookies": response.cookies,
            "headers": response.headers,
        }
