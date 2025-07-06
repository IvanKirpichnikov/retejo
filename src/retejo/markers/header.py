from typing import Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker


class HeaderMarker(BaseMarker):
    name = "Header"


T = TypeVar("T")
Header: TypeAlias = Annotated[T, HeaderMarker()]
