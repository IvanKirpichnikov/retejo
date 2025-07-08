import inspect
from collections.abc import Awaitable, Callable
from typing import Any, Generic, NoReturn, ParamSpec, TypeVar, cast, overload

from retejo.core.entities import Method
from retejo.core.sendable_method import AsyncSendableMethod, SyncSendableMethod

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")


class _BindMethod(Generic[_MethodParamSpec, _MethodResultT]):
    def __init__(
        self,
        method_tp: Callable[_MethodParamSpec, Method[_MethodResultT]],
    ) -> None:
        self._method_tp = method_tp

    @overload
    def __get__(
        self,
        obj: SyncSendableMethod,
        objtype: Any = None,
    ) -> Callable[_MethodParamSpec, _MethodResultT]: ...

    @overload
    def __get__(
        self,
        obj: AsyncSendableMethod,
        objtype: Any = None,
    ) -> Callable[_MethodParamSpec, Awaitable[_MethodResultT]]: ...

    @overload
    def __get__(
        self,
        obj: Any,
        objtype: Any = None,
    ) -> NoReturn: ...

    def __get__(
        self,
        obj: Any,
        objtype: Any = None,
    ) -> Any:
        if not isinstance(obj, SyncSendableMethod | AsyncSendableMethod):
            raise RuntimeError("bind_method use is only (Async | Sync)SendableMethod interfaces")

        if inspect.iscoroutinefunction(obj.send_method):
            async_client = cast("AsyncSendableMethod", obj)

            async def async_wrapper(
                *args: _MethodParamSpec.args,
                **kwargs: _MethodParamSpec.kwargs,
            ) -> _MethodResultT:
                return await async_client.send_method(self._method_tp(*args, **kwargs))

            return async_wrapper
        else:
            sync_client = cast("SyncSendableMethod", obj)

            def sync_wrapper(
                *args: _MethodParamSpec.args,
                **kwargs: _MethodParamSpec.kwargs,
            ) -> _MethodResultT:
                return sync_client.send_method(self._method_tp(*args, **kwargs))

            return sync_wrapper


def bind_method(
    method_tp: Callable[_MethodParamSpec, Method[_MethodResultT]],
) -> _BindMethod[_MethodParamSpec, _MethodResultT]:
    return _BindMethod(method_tp)
