from collections.abc import Awaitable, Callable
from typing import Any, NoReturn, overload

from retejo.interfaces import AsyncSendableMethod, SyncSendableMethod
from retejo.method import Method


class _BindMethod[**P, T]:
    def __init__(
        self,
        method: Callable[P, Method[T]],
    ) -> None:
        self._method = method

    @overload
    def __get__(self, obj: SyncSendableMethod, objtype: Any = None) -> Callable[P, T]: ...

    @overload
    def __get__(
        self, obj: AsyncSendableMethod, objtype: Any = None
    ) -> Callable[P, Awaitable[T]]: ...

    @overload
    def __get__(self, obj: Any, objtype: Any = None) -> NoReturn: ...

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        if isinstance(obj, SyncSendableMethod):

            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return obj.send_method(self._method(*args, **kwargs))

            return sync_wrapper

        if isinstance(obj, AsyncSendableMethod):

            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return await obj.send_method(self._method(*args, **kwargs))

            return async_wrapper

        raise RuntimeError("method_call use is only Session subclasses")
