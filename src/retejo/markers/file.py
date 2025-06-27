from typing import TYPE_CHECKING, Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker, get_value_marker


class FileMarker(BaseMarker):
    pass


T = TypeVar("T")
if TYPE_CHECKING:
    File: TypeAlias = Annotated[T, FileMarker(T)]
else:

    class File:
        def __class_getitem__(cls, tp: T) -> T:
            return Annotated[tp, FileMarker(get_value_marker(tp))]
