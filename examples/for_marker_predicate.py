# ruff: noqa: T201
import logging
from dataclasses import dataclass

from adaptix import NameStyle, P, Retort, dumper, name_mapping
from typing_extensions import override

from retejo.core import AdaptixFactory, Factory, bind_method
from retejo.http import (
    HttpMethod,
    QueryParam,
    QueryParamMarker,
    UrlVar,
    http_response_loader_provider,
)
from retejo.http.clients.requests import RequestsClient
from retejo.marker_tools import for_marker


@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int


class GetPost(HttpMethod[Post]):
    __url__ = "posts/{id}"
    __http_method__ = "get"

    id: UrlVar[int]
    marker: QueryParam[int | None] = None


class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    @override
    def init_response_loader(self) -> Factory:
        retort = Retort(
            recipe=[
                http_response_loader_provider(),
                name_mapping(name_style=NameStyle.CAMEL),
                # Convert all `QueryParam` values `None` to `"null"`
                dumper(
                    for_marker(QueryParamMarker, P[None]),
                    lambda x: "null",
                ),
            ],
        )
        return AdaptixFactory(retort)

    get_post = bind_method(GetPost)


def main() -> None:
    with Client() as client:
        print(client.get_post(id=84))


logging.basicConfig(level=logging.DEBUG)
main()
