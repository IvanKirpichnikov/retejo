from typing import Any
from retejo.adaptix.default_providers import FileObj
from retejo.http.entities import HttpMethod
from retejo.http.integrations.requests import RequestsClient
from retejo.http.markers import Form
from retejo.method_binder import bind_method


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
        client.get_http_bin()

        with open(__file__, "rb") as file:  # noqa: PTH123
            client.upload_image(file=FileObj(contents=file))


main()
