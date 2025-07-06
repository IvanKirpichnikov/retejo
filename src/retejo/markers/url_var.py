from typing import Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker


class UrlVarMarker(BaseMarker):
    name = "UrlVar"


T = TypeVar("T")
UrlVar: TypeAlias = Annotated[T, UrlVarMarker()]
