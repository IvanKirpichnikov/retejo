from typing import Any, TypeAlias, TypeVar

from adaptix import TypeHint
from typing_extensions import TypeIs, override

from retejo._internal.adaptix.type_tools.norm_utils import strip_tag
from retejo._internal.adaptix.type_tools.normalize_type import (
    is_normalize_type,
    soft_normalize_type,
)
from retejo._internal.singleton import SingletonMeta


class Omitted(metaclass=SingletonMeta):
    __slots__ = ()

    def __bool__(self) -> bool:
        return False

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}()>"


_OmittedValueT = TypeVar("_OmittedValueT")
Omittable: TypeAlias = _OmittedValueT | Omitted


def is_omitted(value: Any) -> TypeIs[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[_OmittedValueT]) -> TypeIs[_OmittedValueT]:
    return not is_omitted(value)


def is_defined(value: Omittable[_OmittedValueT | None]) -> TypeIs[_OmittedValueT]:
    return is_not_omitted(value) and value is not None


def is_not_defined(value: Omittable[_OmittedValueT | None]) -> TypeIs[Omittable[None]]:
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


def alert1(lgh: Omittable[_OmittedValueT], rgh: _OmittedValueT) -> _OmittedValueT:
    if isinstance(lgh, Omitted):
        return rgh
    return lgh


def alert2(lgh: _OmittedValueT, rgh: Omittable[_OmittedValueT]) -> _OmittedValueT:
    if isinstance(rgh, Omitted):
        return lgh
    return rgh
