# ruff: noqa: T201
import asyncio
from dataclasses import dataclass

from adaptix import NameStyle, Retort, name_mapping
from typing_extensions import override

from retejo.core import AdaptixFactory, Factory, bind_method
from retejo.http import (
    Body,
    HttpMethod,
    UrlVar,
    http_response_loader_provider,
)
from retejo.http.clients.httpx_async import HttpxAsyncClient
from retejo.http.clients.httpx_sync import HttpxSyncClient


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


class CreatePost(HttpMethod[PostId]):
    __url__ = "posts"
    __http_method__ = "post"

    user_id: Body[int]
    title: Body[str]
    body: Body[str]


class JSONPlaceholderSyncClient(HttpxSyncClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    @override
    def init_response_loader(self) -> Factory:
        retort = Retort(
            recipe=[
                http_response_loader_provider(),
                name_mapping(name_style=NameStyle.CAMEL),
            ],
        )
        return AdaptixFactory(retort)

    get_post = bind_method(GetPost)
    create_post = bind_method(CreatePost)


class JSONPlaceholderAsyncClient(HttpxAsyncClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    @override
    def init_response_loader(self) -> Factory:
        retort = Retort(
            recipe=[
                http_response_loader_provider(),
                name_mapping(name_style=NameStyle.CAMEL),
            ],
        )
        return AdaptixFactory(retort)

    get_post = bind_method(GetPost)
    create_post = bind_method(CreatePost)


def sync_example() -> None:
    print("=== HTTPX Sync Client Example ===")
    with JSONPlaceholderSyncClient() as client:
        # Create a post
        new_post = client.create_post(
            user_id=1,
            title="Hello from httpx sync",
            body="This is a test post using httpx sync client",
        )
        print(f"Created post with ID: {new_post.id}")

        # Get a post
        post = client.get_post(id=1)
        print(f"Retrieved post: ID={post.id}, Title='{post.title}'")


async def async_example() -> None:
    print("\n=== HTTPX Async Client Example ===")
    async with JSONPlaceholderAsyncClient() as client:
        # Create a post
        new_post = await client.create_post(
            user_id=1,
            title="Hello from httpx async",
            body="This is a test post using httpx async client",
        )
        print(f"Created post with ID: {new_post.id}")

        # Get a post
        post = await client.get_post(id=1)
        print(f"Retrieved post: ID={post.id}, Title='{post.title}'")


if __name__ == "__main__":
    sync_example()
    asyncio.run(async_example())
