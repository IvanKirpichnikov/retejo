from typing import Annotated, TypeVar

from retejo.markers.base import BaseMarker, is_marker_factory


class QueryParamMarker(BaseMarker):
    pass


T = TypeVar("T")
QueryParam = Annotated[T, QueryParamMarker()]
is_query_param = is_marker_factory(QueryParamMarker)
