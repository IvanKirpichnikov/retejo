from collections.abc import Callable

from retejo._internal.bind_method import _BindMethod
from retejo.method import Method


def bind_method[**P, T](method: Callable[P, Method[T]]) -> _BindMethod[P, T]:
    return _BindMethod(method)
