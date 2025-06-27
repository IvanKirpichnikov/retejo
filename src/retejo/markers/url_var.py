from typing import TYPE_CHECKING, Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker, get_value_marker


class UrlVarMarker(BaseMarker):
    pass


T = TypeVar("T")
if TYPE_CHECKING:
    UrlVar: TypeAlias = Annotated[T, UrlVarMarker(T)]
else:

    class UrlVar:
        def __class_getitem__(cls, tp: T) -> T:
            return Annotated[tp, UrlVarMarker(get_value_marker(tp))]
