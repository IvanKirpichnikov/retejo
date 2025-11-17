from abc import ABC
from typing import Any, Generic, Mapping, ParamSpec, TypeVar

from typing_extensions import override

from retejo.entities.request_context_proxy import RequestContextProxy
from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.markers import BodyMarker, FormMarker, HeaderMarker, QueryParamMarker, UrlVarMarker
from retejo.http.types import HttpMethodDumperType, HttpMethodResultLoaderType
from retejo.interfaces.client import AsyncClient, SyncClient
from retejo.method_caller import BaseAsyncMethodCaller, BaseSyncMethodCaller
from retejo.method_result_loader import MethodResultLoaderCtx

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")
_RawHttpResponseT = TypeVar("_RawHttpResponseT")


class BaseSyncHttpMethodCaller(
    BaseSyncMethodCaller[
        HttpRequest,
        HttpResponse[_RawHttpResponseT],
        HttpMethod[Any],
        _MethodParamSpec,
        _MethodResultT,
    ],
    Generic[_MethodParamSpec, _MethodResultT, _RawHttpResponseT],
    ABC,
):
    def __init__(
        self,
        method_cls: Any,
        client: SyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawHttpResponseT], Any],
        method_dumper: HttpMethodDumperType,
        method_result_loader: HttpMethodResultLoaderType[_RawHttpResponseT],
    ) -> None:
        super().__init__(
            method_cls=method_cls,
            client=client,
            method_dumper=method_dumper,
            method_result_loader=method_result_loader,
        )

    @override
    def method_to_request(self, method: HttpMethod[Any]) -> HttpRequest:
        dumped_method = self._method_dumper.dump(method)
        request_context = RequestContextProxy(dumped_method)

        request_url = self.formatting_request_url(
            template_url=method.__url__,
            url_vars_map=request_context.get(UrlVarMarker),
        )

        return HttpRequest(
            url=request_url,
            http_method=method.__http_method__,
            body=request_context.get(BodyMarker),
            headers=request_context.get(HeaderMarker),
            query_params=request_context.get(QueryParamMarker),
            form=request_context.get(FormMarker),
            context=request_context,
        )

    def formatting_request_url(
        self,
        template_url: str,
        url_vars_map: Mapping[str, Any] | None,
    ) -> str:
        if url_vars_map is None:
            return template_url
        else:
            return template_url.format_map(url_vars_map)

    @override
    def load_method_result(
        self,
        method: HttpMethod[_MethodResultT],
        request: HttpRequest,
        response: HttpResponse[_RawHttpResponseT],
    ) -> _MethodResultT:
        response_load_data = self.make_response_load_data(response)
        return self._method_result_loader.load(
            data=response_load_data,
            method_result_type_hint=method.__result__,
            ctx=MethodResultLoaderCtx(
                method=method,
                request=request,
                response=response,
            ),
        )

    def make_response_load_data(
        self,
        response: HttpResponse[_RawHttpResponseT],
    ) -> Any:
        return response.body


class BaseAsyncHttpMethodCaller(
    BaseAsyncMethodCaller[
        HttpRequest,
        HttpResponse[_RawHttpResponseT],
        HttpMethod[Any],
        _MethodParamSpec,
        _MethodResultT,
    ],
    ABC,
    Generic[_MethodParamSpec, _MethodResultT, _RawHttpResponseT],
):
    def __init__(
        self,
        method_cls: Any,
        client: AsyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawHttpResponseT], Any],
        method_dumper: HttpMethodDumperType,
        method_result_loader: HttpMethodResultLoaderType[_RawHttpResponseT],
    ) -> None:
        super().__init__(
            method_cls=method_cls,
            client=client,
            method_dumper=method_dumper,
            method_result_loader=method_result_loader,
        )

    @override
    async def method_to_request(self, method: HttpMethod[Any]) -> HttpRequest:
        dumped_method = self._method_dumper.dump(method)
        request_context = RequestContextProxy(dumped_method)

        request_url = self.formatting_request_url(
            template_url=method.__url__,
            url_vars_map=request_context.get(UrlVarMarker),
        )

        return HttpRequest(
            url=request_url,
            http_method=method.__http_method__,
            body=request_context.get(BodyMarker),
            headers=request_context.get(HeaderMarker),
            query_params=request_context.get(QueryParamMarker),
            form=request_context.get(FormMarker),
            context=request_context,
        )

    def formatting_request_url(
        self,
        template_url: str,
        url_vars_map: Mapping[str, Any] | None,
    ) -> str:
        if url_vars_map is None:
            return template_url
        else:
            return template_url.format_map(url_vars_map)

    @override
    async def load_method_result(
        self,
        method: HttpMethod[_MethodResultT],
        request: HttpRequest,
        response: HttpResponse[_RawHttpResponseT],
    ) -> _MethodResultT:
        response_load_data = self.make_response_load_data(response)
        return self._method_result_loader.load(
            data=response_load_data,
            method_result_type_hint=method.__result__,
            ctx=MethodResultLoaderCtx(
                method=method,
                request=request,
                response=response,
            ),
        )

    def make_response_load_data(
        self,
        response: HttpResponse[_RawHttpResponseT],
    ) -> Any:
        return response.body
