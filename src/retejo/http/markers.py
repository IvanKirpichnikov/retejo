from typing import Annotated, TypeAlias, TypeVar

from retejo.core.markers import BaseMarker


class BaseHttpMarker(BaseMarker):
    def __repr__(self) -> str:
        return f"<Http marker {self.name!r}>"


class BodyMarker(BaseHttpMarker):
    name = "Body"


class FileMarker(BaseHttpMarker):
    name = "File"


class HeaderMarker(BaseHttpMarker):
    name = "Header"


class QueryParamMarker(BaseHttpMarker):
    name = "QueryParam"


class UrlVarMarker(BaseHttpMarker):
    name = "UrlVar"


_MarkerValueT = TypeVar("_MarkerValueT")

Body: TypeAlias = Annotated[_MarkerValueT, BodyMarker()]
File: TypeAlias = Annotated[_MarkerValueT, FileMarker()]
Header: TypeAlias = Annotated[_MarkerValueT, HeaderMarker()]
QueryParam: TypeAlias = Annotated[_MarkerValueT, QueryParamMarker()]
UrlVar: TypeAlias = Annotated[_MarkerValueT, UrlVarMarker()]
