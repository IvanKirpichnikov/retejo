import asyncio
import contextlib
import logging
from typing import Final, override

from adaptix import NameStyle, Retort, name_mapping

from methods import (
    CreatePost,
    DeletePost,
    GetHttpBin,
    GetPost,
    ListPosts,
    UploadImage,
)
from retejo.file_obj import FileObj
from retejo.integrations.aiohttp import AiottpClient

from retejo.bind import bind_method


BASE_URL: Final = "https://jsonplaceholder.typicode.com/"


class AsyncClient(AiottpClient):
    def __init__(self) -> None:
        super().__init__(base_url=BASE_URL)

    @override
    def _init_response_factory(self) -> Retort:
        retort = super()._init_response_factory()
        return retort.extend(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ]
        )

    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)

    get_httpbin = bind_method(GetHttpBin)
    upload_image = bind_method(UploadImage)


async def main() -> None:
    client = AsyncClient()

    async with contextlib.aclosing(client):
        print(await client.list_posts())
        print(await client.get_post(84))
        print(await client.delete_post(84))
        print(
            await client.create_post(
                user_id=10,
                title="Retejo",
                body="retejo python wramework",
            )
        )
        print(await client.get_httpbin())
        print(await client.upload_image(file=FileObj(open("async.py", "rb"))))


logging.basicConfig(level=logging.INFO)

asyncio.run(main())
