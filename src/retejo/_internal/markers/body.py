from typing import TYPE_CHECKING, Annotated, Any, TypeVar

from retejo._internal.markers.base import _Marker, is_marker_factory


class _Body(_Marker):
    pass


T = TypeVar("T")

if TYPE_CHECKING:
    type Body[T] = T
else:

    class Body:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, _Body()]


is_body = is_marker_factory(_Body)
