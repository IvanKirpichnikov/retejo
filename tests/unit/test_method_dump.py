from typing import Any

import pytest
from adaptix import P, Retort, as_is_dumper, as_sentinel, bound, dumper, name_mapping

from retejo.file_obj import FileObj
from retejo.markers.body import Body, BodyMarker
from retejo.markers.file import File, FileMarker
from retejo.markers.header import Header, HeaderMarker
from retejo.markers.omitted import Omittable, Omitted
from retejo.markers.query_param import QueryParam, QueryParamMarker
from retejo.markers.url_var import UrlVar, UrlVarMarker
from retejo.method.method import Method
from retejo.utils.method_dumper import MethodDumperProvider
from retejo.utils.predicates.for_marker import ForMarkerPredicate
from retejo.utils.predicates.with_parents import WithParentsPredicate

retort = Retort(
    recipe=[
        as_sentinel(Omitted),
        as_is_dumper(FileObj),
        bound(
            WithParentsPredicate(Method),
            MethodDumperProvider(),
        ),
    ]
)


class ConcreteMethod(Method[Any]):
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
        # (
        #     ConcreteMethod(
        #         omitted_body=None,
        #         body=None,
        #         file=None,
        #         header=None,
        #         query_param=None,
        #         url_var=None,
        #     ),
        #     {
        #         BodyMarker.name: {"body": None, "omitted_body": None},
        #         FileMarker.name: {"file": None},
        #         HeaderMarker.name: {"header": None},
        #         QueryParamMarker.name: {"query_param": None},
        #         UrlVarMarker.name: {"url_var": None},
        #     },
        #     retort,
        # ),
        # (
        #     ConcreteMethod(
        #         omitted_body=Omitted(),
        #         body=None,
        #         file=None,
        #         header=None,
        #         query_param=None,
        #         url_var=None,
        #     ),
        #     {
        #         BodyMarker.name: {"body": None},
        #         FileMarker.name: {"file": None},
        #         HeaderMarker.name: {"token": None},
        #         QueryParamMarker.name: {"query_param": None},
        #         UrlVarMarker.name: {"url_var": None},
        #     },
        #     retort.extend(
        #         recipe=[
        #             name_mapping(
        #                 P[ConcreteMethod],
        #                 map={
        #                     "header": "token",
        #                 },
        #             ),
        #         ],
        #     ),
        # ),
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
                    dumper(P[None] & ForMarkerPredicate(QueryParamMarker), lambda x: "null"),
                ],
            ),
        ),
    ],
)
def test_successful_dump_method(
    method: Method[Any],
    result: Any,
    retort: Retort,
) -> None:
    assert retort.dump(method) == result
