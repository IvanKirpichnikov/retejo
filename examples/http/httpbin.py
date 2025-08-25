# ruff: noqa: T201
import logging
from typing import Any

from retejo.core import bind_method
from retejo.http import FileObj, Form, HttpMethod
from retejo.http.clients.requests import RequestsClient


class GetHttpBin(HttpMethod[Any]):
    __url__ = "get"
    __http_method__ = "get"


class UploadImage(HttpMethod[Any]):
    __url__ = "post"
    __http_method__ = "post"

    file: Form[FileObj]


class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__("https://httpbin.org/")

    get_http_bin = bind_method(GetHttpBin)
    upload_image = bind_method(UploadImage)


def main() -> None:
    with Client() as client:
        print(client.get_http_bin())

        with open("examples/http/httpbin.py", "rb") as file:  # noqa: PTH123
            print(client.upload_image(file=FileObj(file)))


logging.basicConfig(level=logging.DEBUG)
main()
