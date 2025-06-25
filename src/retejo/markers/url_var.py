from typing import Annotated, TypeVar

from retejo.markers.base import BaseMarker, is_marker_factory


class UrlVarMarker(BaseMarker):
    pass


T = TypeVar("T")
UrlVar = Annotated[T, UrlVarMarker()]
is_url_var = is_marker_factory(UrlVarMarker)
