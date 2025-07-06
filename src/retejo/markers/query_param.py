from typing import Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker


class QueryParamMarker(BaseMarker):
    name = "QueryParam"


T = TypeVar("T")
QueryParam: TypeAlias = Annotated[T, QueryParamMarker()]
