from adaptix import TypeHint

from retejo._internal.type_tools.norm_utils import strip_tag
from retejo._internal.type_tools.normalize_type import is_normalize_type, soft_normalize_type
from retejo.core.markers import BaseMarker


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
