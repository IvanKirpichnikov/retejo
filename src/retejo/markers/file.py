from typing import Annotated, TypeVar

from retejo.markers.base import BaseMarker, is_marker_factory


class FileMarker(BaseMarker):
    pass


T = TypeVar("T")
File = Annotated[T, FileMarker()]
is_file = is_marker_factory(FileMarker)
