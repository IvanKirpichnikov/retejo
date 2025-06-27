from typing import TYPE_CHECKING, Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker, get_value_marker


class BodyMarker(BaseMarker):
    pass


T = TypeVar("T")

if TYPE_CHECKING:
    Body: TypeAlias = Annotated[T, BodyMarker(T)]
else:

    class Body:
        def __class_getitem__(cls, tp: T) -> T:
            return Annotated[tp, BodyMarker(get_value_marker(tp))]
