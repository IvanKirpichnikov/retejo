from typing import Any, TypeVar

from adaptix import TypeHint
from typing_extensions import TypeIs

from retejo._internal.type_tools.norm_utils import strip_tag
from retejo._internal.type_tools.normalize_type import is_normalize_type, soft_normalize_type
from retejo.core.markers import Omittable, Omitted

_OmittedValueT = TypeVar("_OmittedValueT")


def is_omitted(value: Any) -> TypeIs[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[_OmittedValueT]) -> TypeIs[_OmittedValueT]:
    return not is_omitted(value)


def is_defined(value: Omittable[_OmittedValueT | None]) -> TypeIs[_OmittedValueT]:
    return not isinstance(value, Omitted) and value is not None


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


def is_not_omittable_tp(tp: TypeHint) -> bool:
    return not is_omittable_tp(tp)
