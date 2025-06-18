from typing import TYPE_CHECKING, Annotated, Any

from retejo._internal.markers.base import BaseMarker, is_marker_factory


class QueryParamMarker(BaseMarker):
    pass


if TYPE_CHECKING:
    type QueryParam[T] = T
else:

    class QueryParam:
        def __class_getitem__(cls, item: Any) -> Any:
            return Annotated[item, QueryParamMarker()]


is_query_param = is_marker_factory(QueryParamMarker)
