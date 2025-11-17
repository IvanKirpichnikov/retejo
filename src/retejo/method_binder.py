from collections.abc import Callable
from typing import Any, Generic, ParamSpec, TypeVar, cast, overload

from typing_extensions import Self, override

from retejo.entities.method import Method
from retejo.interfaces.client import AsyncClient, SyncClient
from retejo.interfaces.method_caller import AsyncMethodCaller, SyncMethodCaller
from retejo.interfaces.method_caller_factory import MethodCallerFactory

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")
_MethodCallerFactoryUnion = (
    MethodCallerFactory[AsyncClient[Any, Any, Any, Any], Any, AsyncMethodCaller[Any, Any]]
    | MethodCallerFactory[SyncClient[Any, Any, Any, Any], Any, SyncMethodCaller[Any, Any]]
)


class MethodBinder(
    Generic[
        _MethodParamSpec,
        _MethodResultT,
    ],
):
    __slots__ = ("_method_caller_factory", "_method_cls")

    def __init__(
        self,
        method_cls: Any,
        method_caller_factory: _MethodCallerFactoryUnion | None,
    ) -> None:
        self._method_cls = method_cls
        self._method_caller_factory = method_caller_factory

    @property
    def method_cls(self) -> Any:
        return self._method_cls

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._method_cls}, {self._method_caller_factory})>"

    @overload
    def __get__(
        self,
        client: None,
        owner: Any = None,
    ) -> Self: ...

    @overload
    def __get__(
        self,
        client: SyncClient[Any, Any, Any, Any],
        owner: Any = None,
    ) -> SyncMethodCaller[_MethodParamSpec, _MethodResultT]: ...

    @overload
    def __get__(
        self,
        client: AsyncClient[Any, Any, Any, Any],
        owner: Any = None,
    ) -> AsyncMethodCaller[_MethodParamSpec, _MethodResultT]: ...

    def __get__(
        self,
        client: Any,
        owner: Any = None,
    ) -> Any:
        if client is None:
            return self

        if not isinstance(client, (AsyncClient, SyncClient)):
            msg = "`bind_method` use is only `SyncClient` or `AsyncClient` subclasses"
            raise RuntimeError(msg)

        method_caller_factory = self._get_method_caller_factory(client)

        return method_caller_factory(client, self._method_cls)

    def _get_method_caller_factory(
        self, client: AsyncClient[Any, Any, Any, Any] | SyncClient[Any, Any, Any, Any]
    ) -> MethodCallerFactory[Any, Any, Any]:
        method_caller_factory = self._method_caller_factory
        if method_caller_factory is None:
            method_caller_factory = cast(
                "MethodCallerFactory[Any, Any, Any]", client.get_method_caller_factory()
            )

        return method_caller_factory


def bind_method(
    method_cls: Callable[_MethodParamSpec, Method[_MethodResultT]],
    /,
    *,
    method_caller_factory: _MethodCallerFactoryUnion | None = None,
) -> MethodBinder[_MethodParamSpec, _MethodResultT]:
    return MethodBinder(method_cls, method_caller_factory)
