from collections.abc import Callable
from typing import Annotated, Any, TypeGuard, get_origin


class _Marker: ...


def _is_marker[T: _Marker](marker: type[T]) -> Callable[[Any], TypeGuard[T]]:
    def wrapper(obj: Any) -> TypeGuard[T]:
        if get_origin(obj) is Annotated:
            return isinstance(obj.__metadata__[0], marker)
        return False

    return wrapper


is_marker = _is_marker(_Marker)
