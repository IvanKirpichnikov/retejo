from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import _Marker, is_marker_factory


class _QueryParam(_Marker):
    pass


if TYPE_CHECKING:
    type QueryParam[T] = T
else:

    class QueryParam:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, _QueryParam()]


is_query_param = is_marker_factory(_QueryParam)
