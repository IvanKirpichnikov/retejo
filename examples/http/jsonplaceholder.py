# ruff: noqa: T201
import asyncio
import logging
from dataclasses import dataclass

from adaptix import NameStyle, Retort, name_mapping
from typing_extensions import override

from retejo.core import AdaptixFactory, Factory, bind_method
from retejo.http import (
    Body,
    HttpMethod,
    QueryParam,
    UrlVar,
    http_response_loader_provider,
)
from retejo.http.clients.aiohttp import AiohttpClient
from retejo.http.clients.requests import RequestsClient


@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int


@dataclass
class PostId:
    id: int


class GetPost(HttpMethod[Post]):
    __url__ = "posts/{id}"
    __http_method__ = "get"

    id: UrlVar[int]


class ListPosts(HttpMethod[list[Post]]):
    __url__ = "posts"
    __http_method__ = "get"


class DeletePost(HttpMethod[None]):
    __url__ = "posts/{id}"
    __http_method__ = "delete"

    id: UrlVar[int]


class CreatePost(HttpMethod[PostId]):
    __url__ = "posts"
    __http_method__ = "post"

    user_id: QueryParam[int]
    title: Body[str]
    body: Body[str]

def init_response_loader() -> Factory:
    retort = Retort(
        recipe=[
            name_mapping(name_style=NameStyle.CAMEL),
            http_response_loader_provider(),
        ],
    )
    return AdaptixFactory(retort)

class Client(RequestsClient):
    base_url = "https://jsonplaceholder.typicode.com/"

    @override
    def init_response_loader(self) -> Factory:
        return init_response_loader()

    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)


class AsyncClient(AiohttpClient):
    base_url = "https://jsonplaceholder.typicode.com/"

    @override
    def init_response_loader(self) -> Factory:
        return init_response_loader()

    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)


async def main() -> None:
    with Client() as client:
        print(client.list_posts())
        print(client.get_post(id=84))
        print(client.delete_post(id=84))
        print(
            client.create_post(
                user_id=10,
                title="Retejo",
                body="retejo python wramework",
            )
        )

    async with AsyncClient() as client:
        print(await client.list_posts())
        print(await client.get_post(id=84))
        print(await client.delete_post(id=84))  # type: ignore[func-returns-value]
        print(
            await client.create_post(
                user_id=10,
                title="Retejo",
                body="retejo python wramework",
            )
        )


logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())
