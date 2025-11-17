from typing import ClassVar, Generic, TypeVar

from retejo.entities.method import Method

_MethodResultT = TypeVar("_MethodResultT")


class HttpMethod(Method[_MethodResultT], Generic[_MethodResultT]):
    __url__: ClassVar[str]
    __http_method__: ClassVar[str]
