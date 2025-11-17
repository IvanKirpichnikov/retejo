from typing import ClassVar

from adaptix import TypeHint

from retejo._internal.adaptix.type_tools.norm_utils import strip_tag
from retejo._internal.adaptix.type_tools.normalize_type import (
    is_normalize_type,
    soft_normalize_type,
)


class Marker:
    __slots__ = ()

    marker_name: ClassVar[str]


def get_marker(type_hint: TypeHint) -> Marker | None:
    norm_type_hint = soft_normalize_type(type_hint)

    for arg in norm_type_hint.args:
        if is_normalize_type(arg):
            arg = arg.source

        if isinstance(arg, Marker):
            return arg

    strip_norm_type_hint = strip_tag(norm_type_hint)
    if strip_norm_type_hint is norm_type_hint:
        return None

    return get_marker(strip_norm_type_hint)
