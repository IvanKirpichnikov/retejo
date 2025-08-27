# ruff: noqa: T201
import logging
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Any

from adaptix import P, Retort
from typing_extensions import override

from retejo.core import AdaptixFactory, Factory, Omittable, Omitted, bind_method
from retejo.core.entities import AnyResult
from retejo.http import (
    FileObj,
    Form,
    HttpMethod,
    http_response_loader_provider,
    mapping_cookie,
    mapping_header,
)
from retejo.http.clients.requests import RequestsClient


@dataclass
class GetHttpBinResult:
    url: str
    origin: IPv4Address
    args: dict[str, Any]

    content_type: str

    cookie_token: Omittable[str] = Omitted()


class GetHttpBin(HttpMethod[GetHttpBinResult]):
    __url__ = "get"
    __http_method__ = "get"


class UploadImage(HttpMethod[AnyResult]):
    __url__ = "post"
    __http_method__ = "post"

    file: Form[FileObj]


class HttpBinClient(RequestsClient):
    def __init__(self) -> None:
        super().__init__("https://httpbin.org/")

    @override
    def init_response_loader(self) -> Factory:
        retort = Retort(
            recipe=[
                http_response_loader_provider(),
                mapping_header(
                    P[GetHttpBinResult].content_type,
                    "Content-Type",
                ),
                mapping_cookie(
                    P[GetHttpBinResult].cookie_token,
                    "Token",
                ),
            ],
        )
        return AdaptixFactory(retort)

    get_http_bin = bind_method(GetHttpBin)
    upload_image = bind_method(UploadImage)


def main() -> None:
    with HttpBinClient() as client:
        print(client.get_http_bin())

        print(client.upload_image(file=FileObj("abc")))


logging.basicConfig(level=logging.DEBUG)
main()
