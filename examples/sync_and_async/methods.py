from dataclasses import dataclass
from typing import Any

from retejo.file_obj import FileObj
from retejo.markers import Body, File, UrlVar
from retejo.method import Method


@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int


@dataclass
class PostId:
    id: int


class GetPost(Method[Post]):
    __url__ = "posts/{id}"
    __method__ = "get"

    id: UrlVar[int]


class ListPosts(Method[list[Post]]):
    __url__ = "posts"
    __method__ = "get"


class DeletePost(Method[None]):
    __url__ = "posts/{id}"
    __method__ = "delete"

    id: UrlVar[int]


class CreatePost(Method[PostId]):
    __url__ = "posts"
    __method__ = "post"

    user_id: Body[int]
    title: Body[str]
    body: Body[str]


class GetHttpBin(Method[Any]):
    __url__ = "https://httpbin.org/get"
    __method__ = "get"


class UploadImage(Method[Any]):
    __url__ = "https://httpbin.org/post"
    __method__ = "post"

    file: File[FileObj]
