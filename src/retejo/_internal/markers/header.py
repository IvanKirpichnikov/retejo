from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import _Marker, is_marker_factory


class _Header(_Marker):
    pass


if TYPE_CHECKING:
    type Header[T] = T
else:

    class Header:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, _Header()]


is_header = is_marker_factory(_Header)
