from typing import Any

from retejo.markers import (
    Body,
    File,
    Header,
    QueryParam,
    UrlVar,
)
from retejo.markers.body import BodyMarker
from retejo.markers.file import FileMarker
from retejo.markers.header import HeaderMarker
from retejo.markers.omitted import Omittable
from retejo.markers.query_param import QueryParamMarker
from retejo.markers.url_var import UrlVarMarker
from retejo.method import Method

markers = [
    BodyMarker,
    FileMarker,
    HeaderMarker,
    QueryParamMarker,
    UrlVarMarker,
]


class ConcreteMethod(Method[Any]):
    __method__ = __url__ = ""

    body: Body[Any]
    file: File[Any]
    header: Header[Any]
    query_param: QueryParam[Any]
    url_var: UrlVar[Any]


class OtherMethod(Method[Any]):
    __method__ = __url__ = ""

    body: Body[Any]
    omittable_body: Body[Omittable[Any]]

    file: File[Any]
    header: Header[Any]

    query_param: QueryParam[Any]
    omittable_query_param: QueryParam[Omittable[Any]]

    url_var: UrlVar[Any]


def test_current_method_context_filled() -> None:
    context = ConcreteMethod.__context__
    for marker in markers:
        assert len(context.fields[marker]) == 1
        assert context.types.get(marker) is not None
