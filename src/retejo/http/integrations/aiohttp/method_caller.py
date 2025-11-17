from typing import Any, Generic, ParamSpec, TypeVar

from aiohttp import ClientResponse
from typing_extensions import override

from retejo.entities.response import Response
from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.method_caller import BaseAsyncHttpMethodCaller
from retejo.http.types import HttpMethodDumperType, HttpMethodResultLoaderType
from retejo.interfaces.client import AsyncClient

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")


class AiohttpMethodCaller(
    BaseAsyncHttpMethodCaller[_MethodParamSpec, _MethodResultT, ClientResponse],
    Generic[_MethodParamSpec, _MethodResultT],
):
    def __init__(
        self,
        method_cls: Any,
        client: AsyncClient[HttpMethod[Any], HttpRequest, HttpResponse[ClientResponse], Any],
        method_dumper: HttpMethodDumperType,
        method_result_loader: HttpMethodResultLoaderType[ClientResponse],
    ) -> None:
        super().__init__(
            method_cls=method_cls,
            client=client,
            method_dumper=method_dumper,
            method_result_loader=method_result_loader,
        )

    @override
    async def is_error_response(self, response: Response[ClientResponse]) -> bool:
        return not response.raw_response.ok
