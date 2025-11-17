from typing import TYPE_CHECKING, Any

from requests import Response
from typing_extensions import override

from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.integrations.requests.method_caller import RequestsMethodCaller
from retejo.method_caller_factory import BaseMethodCallerFactory

if TYPE_CHECKING:
    from retejo.http.integrations.requests.client import RequestsClient


class RequestsMethodCallerFactory(
    BaseMethodCallerFactory[
        "RequestsClient",
        HttpMethod[Any],
        HttpRequest,
        HttpResponse[Response],
        RequestsMethodCaller[..., Any],
    ],
):
    @override
    def __call__(
        self,
        client: "RequestsClient",
        method_cls: type[HttpMethod[Any]],
    ) -> RequestsMethodCaller[..., Any]:
        return RequestsMethodCaller(
            client=client,
            method_cls=method_cls,
            method_dumper=self._method_dumper or client.method_dumper,
            method_result_loader=self._method_result_loader or client.method_result_loader,
        )
