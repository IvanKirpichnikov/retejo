from dataclasses import dataclass

from adaptix import NameStyle, Retort, name_mapping

from retejo.core.factory import AdaptixFactory, Factory
from retejo.core.method_binder import bind_method
from retejo.http.clients.requests import RequestsClient
from retejo.http.entities import HttpMethod
from retejo.http.markers import Body
from retejo.http.providers import http_response_loader_provider


@dataclass(slots=True, frozen=True)
class PostId:
    id: int

class CreatePost(HttpMethod[PostId]):
    __url__ = "posts"
    __method__ = "post"

    user_id: Body[int] # (1)
    title: Body[str]
    body: Body[str]


class JSONPlaceholderClient(RequestsClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    def init_response_loader(self) -> Factory:
        retort = Retort(
            recipe=[
                http_response_loader_provider(),
                name_mapping(name_style=NameStyle.CAMEL) # (1)
            ]
        )
        return AdaptixFactory(retort)

    create_post = bind_method(CreatePost)


def create_post(
    self,
    *,
    user_id: Body[int],
    title: Body[str],
    body: Body[str],
) -> PostId:
    return self.send_method(
        CreatePost(
            user_id=user_id,
            title=title,
            body=body,
        ),
    )


with JSONPlaceholderClient() as client:
    new_post = client.create_post(
        user_id=1,
        title="Hello Retejo",
        body="This is a test post",
    )


client = JSONPlaceholderClient()
new_post = client.create_post(
    user_id=1,
    title="Hello Retejo",
    body="This is a test post",
)
client.close()
