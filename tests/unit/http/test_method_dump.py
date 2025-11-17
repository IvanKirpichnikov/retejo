from typing import Any

import pytest
from adaptix import P, Retort, dumper, name_mapping

from retejo.core.adaptix.for_marker import for_marker
from retejo.core.adaptix.method_provider import method_provider
from retejo.core.entities.base_marker import Omittable, Omitted
from retejo.http.entities import HttpMethod
from retejo.http.markers import (
    Body,
    BodyMarker,
    Form,
    FormMarker,
    Header,
    HeaderMarker,
    QueryParam,
    QueryParamMarker,
    UrlVar,
    UrlVarMarker,
)

retort = Retort(
    recipe=[
        method_provider(),
    ]
)


class ConcreteMethod(HttpMethod[Any]):
    __method__ = __url__ = ""

    omitted_body: Body[Omittable[Any]] = Omitted()
    body: Body[Any]
    file: Form[Any]
    query_param: QueryParam[str | None] = None
    url_var: UrlVar[Any]
    header: Header[Any]


@pytest.mark.parametrize(
    ("method", "result", "retort"),
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
                BodyMarker.name: {"body": None, "omitted_body": None},
                FormMarker.name: {"file": None},
                HeaderMarker.name: {"header": None},
                QueryParamMarker.name: {"query_param": None},
                UrlVarMarker.name: {"url_var": None},
            },
            retort,
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
                BodyMarker.name: {"body": None},
                FormMarker.name: {"file": None},
                HeaderMarker.name: {"token": None},
                QueryParamMarker.name: {"query_param": None},
                UrlVarMarker.name: {"url_var": None},
            },
            retort.extend(
                recipe=[
                    name_mapping(
                        P[ConcreteMethod],
                        map={
                            "header": "token",
                        },
                    ),
                ],
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
                BodyMarker.name: {"body": None},
                FormMarker.name: {"file": None},
                HeaderMarker.name: {"token": None},
                QueryParamMarker.name: {"query_param": "null"},
                UrlVarMarker.name: {"url_var": None},
            },
            retort.extend(
                recipe=[
                    name_mapping(
                        P[ConcreteMethod],
                        map={
                            "header": "token",
                        },
                    ),
                    dumper(
                        for_marker(QueryParamMarker, P[None]),
                        lambda x: "null",
                    ),
                ],
            ),
        ),
    ],
)
def test_successful_dump_method(
    method: HttpMethod[Any],
    result: Any,
    retort: Retort,
) -> None:
    assert retort.dump(method) == result
