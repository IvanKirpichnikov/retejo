import inspect
from collections.abc import Awaitable, Callable, Sequence
from typing import Any, Generic, ParamSpec, TypeVar, cast, overload

from retejo.core.clients import AsyncSendableMethod, SyncSendableMethod
from retejo.core.entities import AnyResult, Method, SequenceResult

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")


class MethodBinder(Generic[_MethodParamSpec, _MethodResultT]):
    __slots__ = ("_method_tp",)

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

    def __get__(
        self,
        instance: Any,
        owner: Any = None,
    ) -> Any:
        if not isinstance(instance, (AsyncSendableMethod, SyncSendableMethod)):
            msg = (
                "`bind_method` use is only `AsyncSendableMethod` or `SyncSendableMethod` interfaces"
            )
            raise RuntimeError(msg)

        if inspect.iscoroutinefunction(instance.send_method):
            async_sendable_method = instance

            async def async_wrapper(  # noqa: WPS430
                *args: _MethodParamSpec.args,
                **kwargs: _MethodParamSpec.kwargs,
            ) -> _MethodResultT:
                return cast(
                    "_MethodResultT",
                    await async_sendable_method.send_method(self._method_tp(*args, **kwargs)),
                )

            return async_wrapper
        else:
            sync_sendable_method = cast("SyncSendableMethod[Any]", instance)

            def sync_wrapper(  # noqa: WPS430
                *args: _MethodParamSpec.args,
                **kwargs: _MethodParamSpec.kwargs,
            ) -> _MethodResultT:
                return cast(
                    "_MethodResultT",
                    sync_sendable_method.send_method(self._method_tp(*args, **kwargs)),
                )

            return sync_wrapper


@overload
def bind_method(
    method_tp: Callable[_MethodParamSpec, Method[AnyResult]],
) -> MethodBinder[_MethodParamSpec, Any]: ...


@overload
def bind_method(
    method_tp: Callable[_MethodParamSpec, Method[SequenceResult[_MethodResultT]]],
) -> MethodBinder[_MethodParamSpec, Sequence[_MethodResultT]]: ...


@overload
def bind_method(
    method_tp: Callable[_MethodParamSpec, Method[_MethodResultT]],
) -> MethodBinder[_MethodParamSpec, _MethodResultT]: ...


def bind_method(method_tp: Any) -> Any:
    return MethodBinder(method_tp)
