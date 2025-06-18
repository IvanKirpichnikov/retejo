from typing import Annotated, Any, TypeGuard, get_args, get_origin

from retejo._internal.markers.base import BaseMarker


class Omitted(BaseMarker):
    def __bool__(self) -> bool | None:
        return False


type Omittable[T] = T | Omitted


def is_omitted(obj: Any) -> TypeGuard[Omitted]:
    return isinstance(obj, Omitted)


def is_omittable(tp: Any) -> TypeGuard[Omittable[Any]]:
    origin = get_origin(tp)

    if origin is Annotated:
        tp = get_args(tp)[0]

    return get_origin(tp) is Omittable
