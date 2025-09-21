from adaptix import NameStyle, Retort, name_mapping
from typing_extensions import override

from retejo.core.factory import AdaptixFactory, Factory
from retejo.core.method_binder import bind_method
from retejo.http.clients.httpx_sync import HttpxSyncClient
from retejo.http.entities import FileObj
from retejo.http.providers import http_response_loader_provider
from tests.e2e.http.conftest import CreatePost, DeletePost, GetPost, ListPosts, PostId, UploadImage


class SyncClient(HttpxSyncClient):
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
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)

    upload_image = bind_method(UploadImage)


def test_lists_posts() -> None:
    with SyncClient() as client:
        list_posts = client.list_posts()
        assert len(list_posts) == 100


def test_get_post() -> None:
    with SyncClient() as client:
        post = client.get_post(id=1)
        assert post.id == 1


def test_delete_post() -> None:
    with SyncClient() as client:
        client.delete_post(id=1)


def test_create_post() -> None:
    with SyncClient() as client:
        post = client.create_post(
            user_id=10,
            title="Retejo",
            body="retejo python wramework",
        )
        assert isinstance(post, PostId)


def test_upload_image() -> None:
    with SyncClient() as client:
        image = client.upload_image(file=FileObj("test"))
        # httpx sends file data in the files field, not form field
        assert image["files"]["file"] == "test" or image["form"]["file"] == "test"
