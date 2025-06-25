from collections.abc import Callable
from typing import Annotated, Any, TypeGuard, TypeVar, get_origin

from retejo._internal.singleton import Singleton


class BaseMarker(metaclass=Singleton):
    pass


T_co = TypeVar("T_co", bound=BaseMarker, covariant=True)


def is_marker_factory(marker: type[T_co]) -> Callable[[Any], TypeGuard[T_co]]:
    def wrapper(obj: Any) -> TypeGuard[T_co]:
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
