from abc import ABC
from typing import (
    Any,
    ClassVar,
    TypeAlias,
    TypeGuard,
    TypeVar,
)

from retejo._type_tools.common import TypeHint
from retejo._type_tools.norm_utils import strip_tag
from retejo._type_tools.normalize_type import is_normalize_type, soft_normalize_type


class BaseMarker(ABC):
    name: ClassVar[str]

    def __repr__(self) -> str:
        return f"<Marker {self.name!r}>"


def get_marker(tp: TypeHint) -> BaseMarker | None:
    norm_tp = soft_normalize_type(tp)

    for arg in norm_tp.args:
        if is_normalize_type(arg):
            arg = arg.source

        if isinstance(arg, BaseMarker):
            return arg

    strip_norm_tp = strip_tag(norm_tp)
    if strip_norm_tp is norm_tp:
        return None

    return get_marker(strip_norm_tp)


class Omitted:
    def __bool__(self) -> bool | None:
        return False

    def __repr__(self) -> str:
        return "<Omitted>"


_OmittedValueT = TypeVar("_OmittedValueT")
Omittable: TypeAlias = _OmittedValueT | Omitted


def is_omitted(value: Any) -> TypeGuard[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[_OmittedValueT]) -> TypeGuard[_OmittedValueT]:
    return not is_omitted(value)


def is_defined(value: Omittable[_OmittedValueT | None]) -> TypeGuard[_OmittedValueT]:
    return not isinstance(value, Omitted) and value is not None


def is_not_defined(value: Omittable[_OmittedValueT | None]) -> TypeGuard[Omittable[None]]:
    return not is_defined(value)


def is_omittable_tp(tp: TypeHint) -> bool:
    norm_tp = soft_normalize_type(tp)
    for arg in norm_tp.args:
        if is_normalize_type(arg):
            arg = arg.source

        if arg is Omitted:
            return True

    strip_norm_tp = strip_tag(norm_tp)
    if strip_norm_tp is norm_tp:
        return False

    return is_omittable_tp(strip_norm_tp)


def is_not_omittable_tp(tp: TypeHint) -> bool:
    return not is_omittable_tp(tp)
