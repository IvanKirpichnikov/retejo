from typing import Annotated, TypeVar

from retejo.markers.base import BaseMarker, is_marker_factory


class BodyMarker(BaseMarker):
    pass


T = TypeVar("T")
Body = Annotated[T, BodyMarker()]
is_body = is_marker_factory(BodyMarker)
