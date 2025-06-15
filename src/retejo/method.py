from collections.abc import Callable
from typing import Any

from retejo.interfaces.method import Method
from retejo.interfaces.session import SendableMethod


class _Method[**P, T]:
    def __init__(
        self,
        method: Callable[P, Method[T]],
    ) -> None:
        self._method = method

    def __get__(self, obj: Any, objtype: Any = None) -> Callable[P, T]:
        if not isinstance(obj, SendableMethod):
            raise RuntimeError("method use is only Session subclasses")

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return obj.send_method(self._method(*args, **kwargs))

        return wrapper


def method[**P, T](method: Callable[P, Method[T]]) -> _Method[P, T]:
    return _Method(method)
