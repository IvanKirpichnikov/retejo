from typing import Annotated, Any

import pytest

from retejo.markers.base import get_markers, get_value_marker
from retejo.markers.body import Body, BodyMarker
from retejo.markers.file import File, FileMarker
from retejo.markers.omitted import Omittable, Omitted
from retejo.markers.url_var import UrlVar, UrlVarMarker


@pytest.mark.parametrize(
    ("obj", "result"),
    [
        (Body[int], [BodyMarker]),
        (UrlVar[Omittable[int]], [UrlVarMarker]),  # type: ignore[misc]
        (Annotated[File[Omittable[int]], object()], [FileMarker]),  # type: ignore[misc]
        (Body[UrlVar[Omittable[int]]], [UrlVarMarker, BodyMarker]),  # type: ignore[misc]
    ],
)
def test_successful_get_markers(obj: Any, result: Any) -> None:
    assert [type(marker) for marker in get_markers(obj)] == result  # type: ignore[union-attr]


@pytest.mark.parametrize(
    ("obj", "result"),
    [
        (Omittable[int], None),  # type: ignore[misc]
    ],
)
def test_unsuccessful_get_markers(obj: Any, result: Any) -> None:
    assert get_markers(obj) == result


@pytest.mark.parametrize(
    ("obj", "result"),
    [
        (Body[int], int),
        (UrlVar[Omittable[int]], int | Omitted),  # type: ignore[misc]
        (Omittable[int], int | Omitted),  # type: ignore[misc]
        (Annotated[File[Omittable[int]], object()], int | Omitted),  # type: ignore[misc]
    ],
)
def test_get_value_marker(obj: Any, result: Any) -> None:
    assert get_value_marker(obj) == result
