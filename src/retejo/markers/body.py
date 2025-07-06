from typing import Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker


class BodyMarker(BaseMarker):
    name = "Body"


T = TypeVar("T")
Body: TypeAlias = Annotated[T, BodyMarker()]
