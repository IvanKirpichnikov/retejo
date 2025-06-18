from collections.abc import Callable
from typing import Annotated, Any, TypeGuard, get_origin


class BaseMarker:
    pass


def is_marker_factory[T: BaseMarker](marker: type[T]) -> Callable[[Any], TypeGuard[T]]:
    def wrapper(obj: Any) -> TypeGuard[T]:
        if get_origin(obj) is Annotated:
            return isinstance(obj.__metadata__[0], marker)
        return False

    return wrapper


def get_marker_type(obj: Any) -> type[BaseMarker] | None:
    if get_origin(obj) is Annotated:
        args = obj.__metadata__
        return type(next(arg for arg in args if isinstance(arg, BaseMarker)))

    return None


is_marker = is_marker_factory(BaseMarker)
