from typing import Annotated, TypeAlias, TypeVar

from typing_extensions import override

from retejo.core.markers import BaseMarker


class BaseHttpMarker(BaseMarker):
    __slots__ = ()

    @override
    def __repr__(self) -> str:
        return f"<Http marker {self.name!r}>"


class BodyMarker(BaseHttpMarker):
    __slots__ = ()

    name = "Body"


class FormMarker(BaseHttpMarker):
    __slots__ = ()

    name = "Form"


class HeaderMarker(BaseHttpMarker):
    __slots__ = ()

    name = "Header"


class QueryParamMarker(BaseHttpMarker):
    __slots__ = ()

    name = "QueryParam"


class UrlVarMarker(BaseHttpMarker):
    __slots__ = ()

    name = "UrlVar"


_MarkerValueT = TypeVar("_MarkerValueT")

Body: TypeAlias = Annotated[_MarkerValueT, BodyMarker()]
Form: TypeAlias = Annotated[_MarkerValueT, FormMarker()]
Header: TypeAlias = Annotated[_MarkerValueT, HeaderMarker()]
QueryParam: TypeAlias = Annotated[_MarkerValueT, QueryParamMarker()]
UrlVar: TypeAlias = Annotated[_MarkerValueT, UrlVarMarker()]
