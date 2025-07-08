from typing import Any

import pytest
from adaptix import P, Retort, as_is_dumper, as_sentinel, dumper, name_mapping

from retejo.core.markers import Omittable, Omitted
from retejo.http.entities import FileObj, HttpMethod
from retejo.http.markers import (
    Body,
    BodyMarker,
    File,
    FileMarker,
    Header,
    HeaderMarker,
    QueryParam,
    QueryParamMarker,
    UrlVar,
    UrlVarMarker,
)
from retejo.utils._fixed_type_hint_tags_unwrapping_provider import FixedTypeHintTagsUnwrappingProvider
from retejo.utils.for_marker import for_marker
from retejo.utils.method_dumper import method_dumper

retort = Retort(
    recipe=[
        as_sentinel(Omitted),
        as_is_dumper(FileObj),
        method_dumper(),
        FixedTypeHintTagsUnwrappingProvider(),
    ]
)


class ConcreteMethod(HttpMethod[Any]):
    __method__ = __url__ = ""

    omitted_body: Body[Omittable[Any]] = Omitted()
    body: Body[Any]
    file: File[Any]
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
                FileMarker.name: {"file": None},
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
                FileMarker.name: {"file": None},
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
                FileMarker.name: {"file": None},
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
                        for_marker(P[None], QueryParamMarker),
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
