from typing import Any, Generic, ParamSpec, TypeVar

from requests import Response
from typing_extensions import override

from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.method_caller import BaseSyncHttpMethodCaller
from retejo.interfaces.client import SyncClient
from retejo.method_dumper import MethodDumper
from retejo.method_result_loader import MethodResultLoader

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")


class RequestsMethodCaller(
    BaseSyncHttpMethodCaller[_MethodParamSpec, _MethodResultT, Response],
    Generic[_MethodParamSpec, _MethodResultT],
):
    def __init__(
        self,
        method_cls: Any,
        client: SyncClient[HttpMethod[Any], HttpRequest, HttpResponse[Response], Any],
        method_dumper: MethodDumper[HttpMethod[Any]],
        method_result_loader: MethodResultLoader[
            HttpMethod[Any], HttpRequest, HttpResponse[Response]
        ],
    ) -> None:
        super().__init__(
            method_cls=method_cls,
            client=client,
            method_dumper=method_dumper,
            method_result_loader=method_result_loader,
        )

    @override
    def is_error_response(self, response: HttpResponse[Response]) -> bool:
        return not response.raw_response.ok
