# ruff: noqa: T201
import asyncio
import logging
from dataclasses import dataclass

from adaptix import NameStyle, Retort, name_mapping

from retejo.adaptix import AdaptixFactory, method_result_loader_provider
from retejo.http.entities import HttpMethod
from retejo.http.integrations.aiohttp import AiohttpClient
from retejo.http.integrations.requests import RequestsClient
from retejo.http.markers import Body, QueryParam, UrlVar
from retejo.method_binder import bind_method
from retejo.method_result_loader import MethodResultLoader


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


method_result_loader = MethodResultLoader(
    AdaptixFactory(
        Retort(
            recipe=[
                method_result_loader_provider(),
                name_mapping(name_style=NameStyle.CAMEL),
            ],
        ),
    ),
)


class MethodsClient:
    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)


class SyncClient(MethodsClient, RequestsClient):
    def __init__(self) -> None:
        super().__init__(
            base_url="https://jsonplaceholder.typicode.com/",
            method_result_loader=method_result_loader,
        )


class AsyncClient(MethodsClient, AiohttpClient):
    def __init__(self) -> None:
        super().__init__(
            base_url="https://jsonplaceholder.typicode.com/",
            method_result_loader=method_result_loader,
        )


async def main() -> None:
    with SyncClient() as client:
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
