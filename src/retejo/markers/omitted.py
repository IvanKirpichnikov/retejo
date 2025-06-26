import types
import typing
from typing import Annotated, Any, TypeAlias, TypeGuard, TypeVar, get_args, get_origin

from retejo._internal.singleton import Singleton


class Omitted(metaclass=Singleton):
    def __bool__(self) -> bool | None:
        return False


T = TypeVar("T")
Omittable: TypeAlias = Annotated[T | Omitted, Omitted()]


def is_omitted(value: Any) -> TypeGuard[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[T]) -> TypeGuard[T]:
    return not is_omitted(value)


def is_defined(value: Omittable[T | None]) -> TypeGuard[T]:
    return not isinstance(value, Omitted) and value is not None


def is_not_defined(value: Omittable[T | None]) -> TypeGuard[Omittable[None]]:
    return not is_defined(value)


def is_omittable(tp: Omittable[T]) -> bool:
    origin = get_origin(tp)
    if (
        origin is Annotated
        and any(isinstance(tp, Omitted) for tp in tp.__metadata__)  # type: ignore[union-attr]
        and (
            get_origin(tp.__origin__) is typing.Union  # type: ignore[union-attr, comparison-overlap]
            or isinstance(tp.__origin__, types.UnionType)  # type: ignore[union-attr]
        )
    ):
        args = get_args(tp.__origin__)  # type: ignore[union-attr]
        if any(issubclass(arg, Omitted) for arg in args):
            return True
    return False


def is_not_omittable(tp: Omittable[T]) -> bool:
    return not is_omittable(tp)
