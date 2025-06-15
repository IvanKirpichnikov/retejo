from typing import Annotated, TypeVar

from retejo.markers.base import _Marker, _is_marker


class _Body(_Marker):
    pass


T = TypeVar("T")
Body = Annotated[T, _Body()]
is_body = _is_marker(_Body)
