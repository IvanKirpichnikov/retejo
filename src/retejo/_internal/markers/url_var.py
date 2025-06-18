from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import BaseMarker, is_marker_factory


class UrlVarMarker(BaseMarker):
    pass


if TYPE_CHECKING:
    type UrlVar[T] = T
else:

    class UrlVar:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, UrlVarMarker()]


is_url_var = is_marker_factory(UrlVarMarker)
