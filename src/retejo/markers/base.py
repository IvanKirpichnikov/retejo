from abc import ABC
from typing import Any, ClassVar

from retejo._adaptix.type_tools.norm_utils import strip_tag
from retejo._adaptix.type_tools.normalize_type import BaseNormType, is_normalize_type, normalize_type


class BaseMarker(ABC):
    name: ClassVar[str]

    def __repr__(self) -> str:
        return f'<Marker "{self.name}">'


def get_marker(tp: Any) -> BaseMarker | None:
    norm_tp = normalize_type(tp) if not isinstance(tp, BaseNormType) else tp

    for arg in norm_tp.args:
        if is_normalize_type(arg):
            arg = arg.source

        if isinstance(arg, BaseMarker):
            return arg

    strip_norm_tp = strip_tag(norm_tp)
    if strip_norm_tp is norm_tp:
        return None

    return get_marker(strip_norm_tp)
