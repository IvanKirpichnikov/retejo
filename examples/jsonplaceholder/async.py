import asyncio
import logging

from adaptix import NameStyle, Retort, name_mapping
from methods import (
    CreatePost,
    DeletePost,
    GetHttpBin,
    GetPost,
    ListPosts,
    UploadImage,
)
from retejo.core.method_binder import bind_method
from retejo.http.clients.aiohttp import AiohttpClient
from retejo.http.entities import FileObj


class AsyncClient(AiohttpClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    def init_response_loader(self) -> Retort:
        response_loader = super().init_response_loader()
        return response_loader.extend(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ],
        )

    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)

    get_httpbin = bind_method(GetHttpBin)
    upload_image = bind_method(UploadImage)


async def main() -> None:
    async with AsyncClient() as client:
        # print(await client.list_posts())
        print(await client.get_post(id=84))
        print(await client.delete_post(id=84))
        print(
            await client.create_post(
                user_id=10,
                title="Retejo",
                body="retejo python wramework",
            )
        )
        print(await client.get_httpbin())
        print(await client.upload_image(file=FileObj(open("async.py", "rb"))))


logging.basicConfig(level=logging.DEBUG)

asyncio.run(main())
