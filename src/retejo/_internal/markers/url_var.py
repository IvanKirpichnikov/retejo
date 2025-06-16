from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import _Marker, is_marker_factory


class _UrlVar(_Marker):
    pass


if TYPE_CHECKING:
    type UrlVar[T] = T
else:

    class UrlVar:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, _UrlVar()]


is_url_var = is_marker_factory(_UrlVar)
