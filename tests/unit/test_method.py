from typing import Any, cast

import pytest

from retejo.markers import (
    Body,
    File,
    Header,
    QueryParam,
    UrlVar,
)
from retejo.markers.base import BaseMarker
from retejo.markers.body import BodyMarker
from retejo.markers.file import FileMarker
from retejo.markers.header import HeaderMarker
from retejo.markers.omitted import Omittable
from retejo.markers.query_param import QueryParamMarker
from retejo.markers.url_var import UrlVarMarker
from retejo.method import Method
from retejo.method.context import MethodContext

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


@pytest.mark.parametrize(
    ("context", "marker_tp", "is_none", "required_keys", "optional_keys"),
    [
        (
            ConcreteMethod.__context__,
            BodyMarker,
            False,
            frozenset(("body",)),
            frozenset(("omittable_body",)),
        ),
        (
            ConcreteMethod.__context__,
            FileMarker,
            False,
            frozenset(("file",)),
            frozenset(),
        ),
        (
            ConcreteMethod.__context__,
            HeaderMarker,
            False,
            frozenset(("header",)),
            frozenset(),
        ),
        (
            ConcreteMethod.__context__,
            QueryParamMarker,
            False,
            frozenset(("query_param",)),
            frozenset(("omittable_query_param",)),
        ),
        (
            ConcreteMethod.__context__,
            UrlVarMarker,
            False,
            frozenset(("url_var",)),
            frozenset(),
        ),
    ],
)
def test_current_method_context_types_filled(
    context: MethodContext,
    marker_tp: type[BaseMarker],
    is_none: bool,
    required_keys: frozenset[str],
    optional_keys: frozenset[str],
) -> None:
    context = OtherMethod.__context__
    types = context.types

    type_for_marker = cast("Any", types[marker_tp])
    if type_for_marker is None:
        assert is_none
    else:
        assert type_for_marker.__required_keys__ == required_keys
        assert type_for_marker.__optional_keys__ == optional_keys
