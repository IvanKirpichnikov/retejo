from adaptix import NameStyle, Retort, name_mapping

from retejo.core.method_binder import bind_method
from retejo.http.clients.aiohttp import AiohttpClient
from retejo.http.entities import FileObj
from tests.e2e.http.conftest import CreatePost, DeletePost, GetPost, ListPosts, PostId, UploadImage


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
