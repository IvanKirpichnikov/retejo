from typing import TYPE_CHECKING, Annotated, TypeAlias, TypeVar

from retejo.markers.base import BaseMarker, get_value_marker


class QueryParamMarker(BaseMarker):
    pass


T = TypeVar("T")
if TYPE_CHECKING:
    QueryParam: TypeAlias = Annotated[T, QueryParamMarker(T)]
else:

    class QueryParam:
        def __class_getitem__(cls, tp: T) -> T:
            return Annotated[tp, QueryParamMarker(get_value_marker(tp))]
