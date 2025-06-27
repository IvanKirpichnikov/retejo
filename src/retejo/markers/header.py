from typing import TYPE_CHECKING, Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker, get_value_marker


class HeaderMarker(BaseMarker):
    pass


T = TypeVar("T")

if TYPE_CHECKING:
    Header: TypeAlias = Annotated[T, HeaderMarker(T)]
else:

    class Header:
        def __class_getitem__(cls, tp: T) -> T:
            return Annotated[tp, HeaderMarker(get_value_marker(tp))]
