from typing import Any, TypeGuard, get_args, get_origin

from retejo.markers.base import BaseMarker


class Omitted(BaseMarker):
    def __bool__(self) -> bool | None:
        return False


type Omittable[T] = T | Omitted


def is_omitted(value: Any) -> TypeGuard[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted[T](value: Omittable[T]) -> TypeGuard[T]:
    return not isinstance(value, Omitted)


def is_defined[T](value: Omittable[T | None]) -> TypeGuard[T]:
    return not isinstance(value, Omitted) or value is not None


def is_omittable(tp: Any) -> TypeGuard[Omittable[Any]]:
    origin = get_origin(tp)
    if origin is Omittable:
        return True

    if origin:
        args = get_args(tp)
        if args:
            return is_omittable(args[0])

    return False
