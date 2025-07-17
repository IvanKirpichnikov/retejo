from dataclasses import dataclass
from typing import Any

from retejo.http.entities import FileObj, HttpMethod
from retejo.http.markers import Body, Form, UrlVar


@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int


@dataclass
class PostId:
    id: int


class GetPost(HttpMethod[Post]):
    __url__ = "posts/{id}"
    __http_method__ = "get"

    id: UrlVar[int]


class ListPosts(HttpMethod[list[Post]]):
    __url__ = "posts"
    __http_method__ = "get"


class DeletePost(HttpMethod[None]):
    __url__ = "posts/{id}"
    __http_method__ = "delete"

    id: UrlVar[int]


class CreatePost(HttpMethod[PostId]):
    __url__ = "posts"
    __http_method__ = "post"

    user_id: Body[int]
    title: Body[str]
    body: Body[str]


class UploadImage(HttpMethod[Any]):
    __url__ = "https://httpbin.org/post"
    __http_method__ = "post"

    file: Form[FileObj]
