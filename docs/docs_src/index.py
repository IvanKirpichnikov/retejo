from dataclasses import dataclass

from adaptix import NameStyle, Retort, name_mapping

from retejo.core import AdaptixFactory, Factory, bind_method
from retejo.http import HttpMethod, http_response_loader_provider, Body
from retejo.http.clients.requests import RequestsClient


@dataclass(slots=True, frozen=True)
class PostId:
    id: int

class CreatePost(HttpMethod[PostId]):
    __url__ = "posts"
    __method__ = "post"

    user_id: Body[int]
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

    create_post = bind_method(CreatePost) # (2)
