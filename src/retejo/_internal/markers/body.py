from typing import TYPE_CHECKING, Annotated, Any, TypeVar

from retejo._internal.markers.base import BaseMarker, is_marker_factory


class BodyMarker(BaseMarker):
    pass


T = TypeVar("T")

if TYPE_CHECKING:
    type Body[T] = T
else:

    class Body:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, BodyMarker()]


is_body = is_marker_factory(BodyMarker)
