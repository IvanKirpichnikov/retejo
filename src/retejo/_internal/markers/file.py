from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import BaseMarker, is_marker_factory


class FileMarker(BaseMarker):
    pass


if TYPE_CHECKING:
    type File[T] = T
else:

    class File:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, FileMarker()]


is_file = is_marker_factory(FileMarker)
