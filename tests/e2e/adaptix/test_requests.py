from adaptix import NameStyle, Retort, name_mapping

from examples.sync_and_async.methods import (
    CreatePost,
    DeletePost,
    GetPost,
    ListPosts,
    PostId,
    UploadImage,
)
from retejo.bind_method import bind_method
from retejo.file_obj import FileObj
from retejo.integrations.adaptix.requests import RequestsAdaptixClient


class AsyncClient(RequestsAdaptixClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    def init_response_factory(self) -> Retort:
        result = super().init_response_factory()
        return result.extend(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ]
        )

    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)

    upload_image = bind_method(UploadImage)


def test_lists_posts() -> None:
    with AsyncClient() as client:
        list_posts = client.list_posts()
        assert len(list_posts) == 100


def test_get_post() -> None:
    with AsyncClient() as client:
        post = client.get_post(1)
        assert post.id == 1


def test_delete_post() -> None:
    with AsyncClient() as client:
        client.delete_post(1)


def test_create_post() -> None:
    with AsyncClient() as client:
        post = client.create_post(
            user_id=10,
            title="Retejo",
            body="retejo python wramework",
        )
        assert isinstance(post, PostId)


def test_upload_image() -> None:
    with AsyncClient() as client:
        image = client.upload_image(FileObj("test"))
        assert image["files"]["file"] == "test"
