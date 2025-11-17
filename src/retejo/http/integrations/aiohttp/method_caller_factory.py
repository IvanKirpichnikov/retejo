from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponse
from typing_extensions import override

from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.integrations.aiohttp.method_caller import AiohttpMethodCaller
from retejo.method_caller_factory import BaseMethodCallerFactory

if TYPE_CHECKING:
    from retejo.http.integrations.aiohttp.client import AiohttpClient


class AiohttpMethodCallerFactory(
    BaseMethodCallerFactory[
        "AiohttpClient",
        HttpMethod[Any],
        HttpRequest,
        HttpResponse[ClientResponse],
        AiohttpMethodCaller[..., Any],
    ],
):
    @override
    def __call__(
        self,
        client: "AiohttpClient",
        method_cls: type[HttpMethod[Any]],
    ) -> AiohttpMethodCaller[..., Any]:
        return AiohttpMethodCaller(
            client=client,
            method_cls=method_cls,
            method_dumper=self._method_dumper or client.method_dumper,
            method_result_loader=self._method_result_loader or client.method_result_loader,
        )
