from typing import Annotated, TypeVar

from retejo.markers.base import _Marker, _is_marker


class _UrlVar(_Marker):
    pass


T = TypeVar("T")
UrlVar = Annotated[T, _UrlVar()]
is_url_var = _is_marker(_UrlVar)
