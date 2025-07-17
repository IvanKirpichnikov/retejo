import inspect
from collections.abc import Awaitable, Callable
from typing import Any, Generic, NoReturn, ParamSpec, TypeVar, cast, overload

from retejo.core.clients import AsyncSendableMethod, SyncSendableMethod
from retejo.core.entities import Method

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
        instance: SyncSendableMethod[Any],
        owner: Any = None,
    ) -> Callable[_MethodParamSpec, _MethodResultT]: ...

    @overload
    def __get__(
        self,
        instance: AsyncSendableMethod[Any],
        owner: Any = None,
    ) -> Callable[_MethodParamSpec, Awaitable[_MethodResultT]]: ...

    @overload
    def __get__(
        self,
        instance: Any,
        owner: Any = None,
    ) -> NoReturn: ...

    def __get__(
        self,
        instance: Any,
        owner: Any = None,
    ) -> Any:
        if not isinstance(instance, (AsyncSendableMethod, SyncSendableMethod)):
            raise RuntimeError("bind_method use is only AsyncClient or SyncClient interfaces")

        if inspect.iscoroutinefunction(instance.send_method):
            async_client = instance

            async def async_wrapper(  # noqa: WPS430
                *args: _MethodParamSpec.args,
                **kwargs: _MethodParamSpec.kwargs,
            ) -> _MethodResultT:
                return await async_client.send_method(self._method_tp(*args, **kwargs))

            return async_wrapper
        else:
            sync_client = cast("SyncSendableMethod[Any]", instance)

            def sync_wrapper(  # noqa: WPS430
                *args: _MethodParamSpec.args,
                **kwargs: _MethodParamSpec.kwargs,
            ) -> _MethodResultT:
                return sync_client.send_method(self._method_tp(*args, **kwargs))

            return sync_wrapper


def bind_method(
    method_tp: Callable[_MethodParamSpec, Method[_MethodResultT]],
) -> _BindMethod[_MethodParamSpec, _MethodResultT]:
    return _BindMethod(method_tp)
