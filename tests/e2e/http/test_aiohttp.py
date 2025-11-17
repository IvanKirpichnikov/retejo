from adaptix import NameStyle, Retort, name_mapping
from typing_extensions import override

from retejo.core import AdaptixFactory, Factory, bind_method
from retejo.http import FileObj, http_response_loader_provider
from retejo.http.integrations.aiohttp import AiohttpClient
from tests.e2e.http.conftest import CreatePost, DeletePost, GetPost, ListPosts, PostId, UploadImage


class AsyncClient(AiohttpClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    @override
    def init_response_loader(self) -> Factory:
        retort = Retort(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
                http_response_loader_provider(),
            ],
        )
        return AdaptixFactory(retort)

    get_post = bind_method(GetPost)
    list_posts = bind_method(ListPosts)
    delete_post = bind_method(DeletePost)
    create_post = bind_method(CreatePost)

    upload_image = bind_method(UploadImage)


async def test_lists_posts() -> None:
    async with AsyncClient() as client:
        list_posts = await client.list_posts()
        assert len(list_posts) == 100


async def test_get_post() -> None:
    async with AsyncClient() as client:
        post = await client.get_post(id=1)
        assert post.id == 1


async def test_delete_post() -> None:
    async with AsyncClient() as client:
        await client.delete_post(id=1)


async def test_create_post() -> None:
    async with AsyncClient() as client:
        post = await client.create_post(
            user_id=10,
            title="Retejo",
            body="retejo python wramework",
        )
        assert isinstance(post, PostId)


async def test_upload_image() -> None:
    async with AsyncClient() as client:
        image = await client.upload_image(file=FileObj("test"))
        assert image["form"]["file"] == "test"
