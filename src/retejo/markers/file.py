from typing import Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker


class FileMarker(BaseMarker):
    name = "File"


T = TypeVar("T")
File: TypeAlias = Annotated[T, FileMarker()]
