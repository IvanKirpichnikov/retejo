from typing import Annotated, TypeVar

from retejo.markers.base import _Marker, _is_marker


class _File(_Marker):
    pass


T = TypeVar("T")
File = Annotated[T, _File()]
is_file = _is_marker(_File)
