from typing import Any

import pytest

from retejo.interfaces.request_context_builder import RequestContext, RequestContextBuilder
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
from retejo.markers.omitted import Omittable, Omitted
from retejo.markers.query_param import QueryParamMarker
from retejo.markers.url_var import UrlVarMarker
from retejo.method.method import Method
from retejo.request_context_builder import SimpleRequestContextBuilder
from tests.utils.exclude_omittable_factory import ExludeOmittableFactory


class ConcreteMethod(Method[Any]):
    __method__ = __url__ = ""

    omitted_body: Body[Omittable[Any]]
    body: Body[Any]
    file: File[Any]
    header: Header[Any]
    query_param: QueryParam[Any]
    url_var: UrlVar[Any]


@pytest.mark.parametrize(
    ("method", "request_context", "builder"),
    [
        (
            ConcreteMethod(
                omitted_body=None,
                body=None,
                file=None,
                header=None,
                query_param=None,
                url_var=None,
            ),
            {
                BodyMarker: {"body": None, "omitted_body": None},
                FileMarker: {"file": None},
                HeaderMarker: {"header": None},
                QueryParamMarker: {"query_param": None},
                UrlVarMarker: {"url_var": None},
            },
            SimpleRequestContextBuilder(
                {
                    BodyMarker: ExludeOmittableFactory(),
                }
            ),
        ),
        (
            ConcreteMethod(
                omitted_body=Omitted(),
                body=None,
                file=None,
                header=None,
                query_param=None,
                url_var=None,
            ),
            {
                BodyMarker: {"body": None},
                FileMarker: {"file": None},
                HeaderMarker: {"header": None},
                QueryParamMarker: {"query_param": None},
                UrlVarMarker: {"url_var": None},
            },
            SimpleRequestContextBuilder(
                {
                    BodyMarker: ExludeOmittableFactory(),
                }
            ),
        ),
    ],
)
def test_successful_request_context_build(
    method: Method[Any],
    request_context: RequestContext,
    builder: RequestContextBuilder,
) -> None:
    assert builder.build(method) == request_context
