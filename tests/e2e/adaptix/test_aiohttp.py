from adaptix import NameStyle, Retort, name_mapping

from retejo.bind_method import bind_method
from retejo.file_obj import FileObj
from retejo.integrations.adaptix.aiohttp import AiohttpAdaptixClient
from tests.e2e.methods import CreatePost, DeletePost, GetPost, ListPosts, PostId, UploadImage


class AsyncClient(AiohttpAdaptixClient):
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


async def test_lists_posts() -> None:
    async with AsyncClient() as client:
        list_posts = await client.list_posts()
        assert len(list_posts) == 100


async def test_get_post() -> None:
    async with AsyncClient() as client:
        post = await client.get_post(1)
        assert post.id == 1


async def test_delete_post() -> None:
    async with AsyncClient() as client:
        await client.delete_post(1)


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
        image = await client.upload_image(FileObj("test"))
        assert image["form"]["file"] == "test"
