import inspect
from collections.abc import Awaitable, Callable
from typing import Any, Generic, NoReturn, ParamSpec, TypeVar, cast, overload

from retejo.interfaces import AsyncSendableMethod, SyncSendableMethod
from retejo.method import Method

T = TypeVar("T")
P = ParamSpec("P")


class _BindMethod(Generic[P, T]):
    def __init__(
        self,
        method: Callable[P, Method[T]],
    ) -> None:
        self._method = method

    @overload
    def __get__(self, obj: SyncSendableMethod, objtype: Any = None) -> Callable[P, T]: ...

    @overload
    def __get__(self, obj: AsyncSendableMethod, objtype: Any = None) -> Callable[P, Awaitable[T]]: ...

    @overload
    def __get__(self, obj: Any, objtype: Any = None) -> NoReturn: ...

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        if not isinstance(obj, SyncSendableMethod | AsyncSendableMethod):
            raise RuntimeError("method_call use is only Session subclasses")

        if inspect.iscoroutinefunction(obj.send_method):
            async_client = cast("AsyncSendableMethod", obj)

            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return await async_client.send_method(self._method(*args, **kwargs))

            return async_wrapper
        else:
            sync_client = cast("SyncSendableMethod", obj)

            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return sync_client.send_method(self._method(*args, **kwargs))

            return sync_wrapper


def bind_method(method: Callable[P, Method[T]]) -> _BindMethod[P, T]:
    return _BindMethod(method)
