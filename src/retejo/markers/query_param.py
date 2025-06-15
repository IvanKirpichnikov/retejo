from typing import Annotated, TypeVar

from retejo.markers.base import _Marker, _is_marker


class _QueryParam(_Marker):
    pass


T = TypeVar("T")
QueryParam = Annotated[T, _QueryParam()]
is_query_param = _is_marker(_QueryParam)
