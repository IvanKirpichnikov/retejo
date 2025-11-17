# ruff: noqa: T201
import logging
from dataclasses import dataclass

from adaptix import NameStyle, P, Retort, dumper, name_mapping

from retejo.adaptix import for_marker, method_dumper_provider, method_result_loader_provider
from retejo.adaptix.factory import AdaptixFactory
from retejo.http.entities import HttpMethod
from retejo.http.integrations.requests import RequestsClient
from retejo.http.markers import QueryParam, UrlVar
from retejo.method_binder import bind_method
from retejo.method_caller import MethodDumper
from retejo.method_result_loader import MethodResultLoader


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
    get_post = bind_method(GetPost)

    def __init__(self) -> None:
        super().__init__(
            base_url="https://jsonplaceholder.typicode.com/",
            method_dumper=MethodDumper(
                AdaptixFactory(
                    Retort(
                        recipe=[
                            method_dumper_provider(),
                            # Convert all `QueryParam` values `None` to `"null"`
                            dumper(
                                for_marker(QueryParam, P[None]),
                                lambda x: "null",
                            ),
                        ],
                    ),
                ),
            ),
            method_result_loader=MethodResultLoader(
                AdaptixFactory(
                    Retort(
                        recipe=[
                            method_result_loader_provider(),
                            name_mapping(name_style=NameStyle.CAMEL),
                        ],
                    ),
                ),
            ),
        )


def main() -> None:
    with Client() as client:
        print(client.get_post(id=84))


logging.basicConfig(level=logging.DEBUG)
main()
