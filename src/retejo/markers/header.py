from typing import Annotated, TypeVar

from retejo.markers.base import BaseMarker, is_marker_factory


class HeaderMarker(BaseMarker):
    pass


T = TypeVar("T")
Header = Annotated[T, HeaderMarker()]
is_header = is_marker_factory(HeaderMarker)
