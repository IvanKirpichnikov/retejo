from dataclasses import dataclass
from types import NoneType
from typing import Any, Generic, TypeVar, overload

from typing_extensions import override

from retejo.entities.method import Method
from retejo.entities.request import Request
from retejo.entities.response import Response
from retejo.interfaces.factory import Factory

_TypeHintT = TypeVar("_TypeHintT")

_MethodT = TypeVar("_MethodT", bound=Method[Any])
_RequestT = TypeVar("_RequestT", bound=Request)
_ResponseT = TypeVar("_ResponseT", bound=Response[Any])


@dataclass(slots=True, frozen=True)
class MethodResultLoaderCtx(Generic[_MethodT, _RequestT, _ResponseT]):
    method: _MethodT
    request: _RequestT
    response: _ResponseT


class MethodResultLoader(Generic[_MethodT, _RequestT, _ResponseT]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Factory) -> None:
        self._factory = factory

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._factory!r})>"

    @property
    def factory(self) -> Factory:
        return self._factory

    @overload
    def load(
        self,
        data: Any,
        method_result_type_hint: type[_TypeHintT],
        ctx: MethodResultLoaderCtx[_MethodT, _RequestT, _ResponseT],
    ) -> _TypeHintT: ...

    @overload
    def load(
        self,
        data: Any,
        method_result_type_hint: Any,
        ctx: MethodResultLoaderCtx[_MethodT, _RequestT, _ResponseT],
    ) -> Any: ...

    def load(
        self,
        data: Any,
        method_result_type_hint: Any,
        ctx: MethodResultLoaderCtx[_MethodT, _RequestT, _ResponseT],
    ) -> Any:
        if method_result_type_hint is Any:
            return ctx.response.raw_result

        if method_result_type_hint is None or method_result_type_hint is NoneType:
            return None

        return self._factory.load(data, method_result_type_hint)
