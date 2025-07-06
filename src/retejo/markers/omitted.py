from typing import (
    Any,
    TypeAlias,
    TypeGuard,
    TypeVar,
)

from retejo._adaptix.type_tools.norm_utils import strip_tag
from retejo._adaptix.type_tools.normalize_type import BaseNormType, is_normalize_type, normalize_type


class Omitted:
    def __bool__(self) -> bool | None:
        return False

    def __repr__(self) -> str:
        return "<Omitted>"


T = TypeVar("T")
Omittable: TypeAlias = T | Omitted


def is_omitted(value: Any) -> TypeGuard[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[T]) -> TypeGuard[T]:
    return not is_omitted(value)


def is_defined(value: Omittable[T | None]) -> TypeGuard[T]:
    return not isinstance(value, Omitted) and value is not None


def is_not_defined(value: Omittable[T | None]) -> TypeGuard[Omittable[None]]:
    return not is_defined(value)


def is_omittable_tp(tp: Any) -> bool:
    norm_tp = normalize_type(tp) if not isinstance(tp, BaseNormType) else tp
    for arg in norm_tp.args:
        if is_normalize_type(arg):
            arg = arg.source

        if arg is Omitted:
            return True

    strip_norm_tp = strip_tag(norm_tp)
    if strip_norm_tp is norm_tp:
        return False

    return is_omittable_tp(strip_norm_tp)


def is_not_omittable_tp(tp: Any) -> bool:
    return not is_omittable_tp(tp)
