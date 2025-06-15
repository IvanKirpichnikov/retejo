from typing import Annotated, TypeVar

from retejo.markers.base import _Marker, _is_marker


class _Header(_Marker):
    pass


T = TypeVar("T")
Header = Annotated[T, _Header()]
is_header = _is_marker(_Header)
