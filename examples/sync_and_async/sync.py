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

from retejo import bind_method
from retejo.clients.requests import RequestsClient
from retejo.file_obj import FileObj


class Client(RequestsClient):
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


def main() -> None:
    with Client() as client:
        print(client.list_posts())
        print(client.get_post(id=84))
        print(client.delete_post(id=84))  # type: ignore[func-returns-value]
        print(
            client.create_post(
                user_id=10,
                title="Retejo",
                body="retejo python wramework",
            )
        )
        print(client.get_httpbin())
        print(client.upload_image(file=FileObj(open("sync.py", "rb"))))


logging.basicConfig(level=logging.DEBUG)
main()
