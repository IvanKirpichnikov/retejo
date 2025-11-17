import inspect
from abc import ABC
from types import TracebackType
from typing import Any, ClassVar, Generic, MutableSequence, Sequence, TypeVar

from typing_extensions import Self, override

from retejo.entities.method import Method
from retejo.entities.request import Request
from retejo.entities.response import Response
from retejo.interfaces.client import AsyncClient, SyncClient
from retejo.method_binder import MethodBinder

_MethodT = TypeVar("_MethodT", bound=Method[Any])
_ResponseT = TypeVar("_ResponseT", bound=Response[Any])
_RequestT_contra = TypeVar("_RequestT_contra", bound=Request, contravariant=True)
_RawResponseT = TypeVar("_RawResponseT")


def _resolve_methods(cls: Any) -> list[type[Method[Any]]]:
    members = inspect.getmembers(cls)
    methods = []

    for _, member in members:
        if isinstance(member, MethodBinder):
            methods.append(member.method_cls)

    return methods


class BaseAsyncClient(
    AsyncClient[_MethodT, _RequestT_contra, _ResponseT, _RawResponseT],
    Generic[_MethodT, _RequestT_contra, _ResponseT, _RawResponseT],
    ABC,
):
    _methods: ClassVar[MutableSequence[type[Method[Any]]]]

    __slots__ = ()

    @override
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._methods = _resolve_methods(cls)

    @override
    @classmethod
    def register_method(cls, method_cls: type[Method[Any]]) -> None:
        cls._methods.append(method_cls)

    @override
    @classmethod
    def get_registred_methods(cls) -> Sequence[type[Method[Any]]]:
        return tuple(cls._methods)

    @override
    async def aclose(self) -> None:
        await self.close()

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()


class BaseSyncClient(
    SyncClient[_MethodT, _RequestT_contra, _ResponseT, _RawResponseT],
    Generic[_MethodT, _RequestT_contra, _ResponseT, _RawResponseT],
    ABC,
):
    _methods: ClassVar[MutableSequence[type[Method[Any]]]]

    __slots__ = ()

    @override
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._methods = _resolve_methods(cls)

    @override
    @classmethod
    def register_method(cls, method_cls: type[Method[Any]]) -> None:
        cls._methods.append(method_cls)

    @override
    @classmethod
    def get_registred_methods(cls) -> Sequence[type[Method[Any]]]:
        return tuple(cls._methods)

    @override
    def __enter__(self) -> Self:
        return self

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
