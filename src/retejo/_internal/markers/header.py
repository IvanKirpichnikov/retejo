from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import BaseMarker, is_marker_factory


class HeaderMarker(BaseMarker):
    pass


if TYPE_CHECKING:
    type Header[T] = T
else:

    class Header:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, HeaderMarker()]


is_header = is_marker_factory(HeaderMarker)
