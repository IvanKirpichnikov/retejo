import contextlib
import logging
from typing import override

from adaptix import NameStyle, Retort, name_mapping
from methods import (
    CreatePost,
    DeletePost,
    GetHttpBin,
    GetPost,
    ListPosts,
    UploadImage,
)

from retejo.bind_method import bind_method
from retejo.file_obj import FileObj
from retejo.integrations.adaptix.requests import RequestsAdaptixClient
from retejo.interfaces import Factory


class Client(RequestsAdaptixClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    @override
    def init_response_factory(self) -> Factory:
        return Retort(
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


def main() -> None:
    client = Client()

    with contextlib.closing(client):
        print(client.list_posts())
        print(client.get_post(84))
        print(client.delete_post(84))
        print(
            client.create_post(
                user_id=10,
                title="Retejo",
                body="retejo python wramework",
            )
        )
        print(client.get_httpbin())
        print(client.upload_image(file=FileObj(open("sync.py", "rb"))))


logging.basicConfig(level=logging.INFO)
main()
