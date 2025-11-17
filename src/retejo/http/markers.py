from typing import Annotated, TypeAlias, TypeVar

from retejo.entities.marker import Marker


class BodyMarker(Marker):
    __slots__ = ()

    marker_name = "Body"


class FormMarker(Marker):
    __slots__ = ()

    marker_name = "Form"


class HeaderMarker(Marker):
    __slots__ = ()

    marker_name = "Header"


class QueryParamMarker(Marker):
    __slots__ = ()

    marker_name = "QueryParam"


class UrlVarMarker(Marker):
    __slots__ = ()

    marker_name = "UrlVar"


_MarkerValueT = TypeVar("_MarkerValueT")


Body: TypeAlias = Annotated[_MarkerValueT, BodyMarker()]
Form: TypeAlias = Annotated[_MarkerValueT, FormMarker()]
Header: TypeAlias = Annotated[_MarkerValueT, HeaderMarker()]
QueryParam: TypeAlias = Annotated[_MarkerValueT, QueryParamMarker()]
UrlVar: TypeAlias = Annotated[_MarkerValueT, UrlVarMarker()]
