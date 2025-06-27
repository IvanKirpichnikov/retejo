from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    TypeAlias,
    TypeGuard,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from .base import get_value_marker


class OmittedMarker:
    origin_tp: Any

    def __init__(self, origin_tp: Any) -> None:
        self.origin_tp = origin_tp


class Omitted:
    def __bool__(self) -> bool | None:
        return False


T = TypeVar("T")

if TYPE_CHECKING:
    Omittable: TypeAlias = T | Omitted
else:

    class Omittable:
        def __class_getitem__(cls, tp: T) -> T | Omitted:
            return Annotated[tp | Omitted, OmittedMarker(Union[get_value_marker(tp), Omitted])]  # noqa: UP007


def is_omitted(value: Any) -> TypeGuard[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[T]) -> TypeGuard[T]:
    return not is_omitted(value)


def is_defined(value: Omittable[T | None]) -> TypeGuard[T]:
    return not isinstance(value, Omitted) and value is not None


def is_not_defined(value: Omittable[T | None]) -> TypeGuard[Omittable[None]]:
    return not is_defined(value)


def is_omittable(tp: Omittable[T]) -> bool:
    res = get_value_marker(tp)

    if get_origin(res) is Union:
        return next((True for arg in get_args(res) if arg is Omitted), False)

    return False


def is_not_omittable(tp: Omittable[T]) -> bool:
    return not is_omittable(tp)
