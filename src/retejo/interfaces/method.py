from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Protocol, dataclass_transform, runtime_checkable


class HTTPMethod(StrEnum):
    GET = "get"
    PUT = "put"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"


@dataclass_transform(
    frozen_default=True,
)
def method_type[T](cls: type[T]) -> type[T]:
    return dataclass(
        frozen=True,
        slots=True,
    )(cls)


@method_type
@runtime_checkable
class Method[T](Protocol):
    __url__: ClassVar[str]
    __returning__: ClassVar[type[T]]  # type: ignore[misc]
    __http_method__: ClassVar[HTTPMethod]
