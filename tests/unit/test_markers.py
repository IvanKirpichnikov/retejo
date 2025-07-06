from typing import Annotated, Any

import pytest

from retejo.markers.base import get_marker
from retejo.markers.body import Body, BodyMarker
from retejo.markers.file import File, FileMarker
from retejo.markers.omitted import (
    Omittable,
    Omitted,
    is_defined,
    is_not_defined,
    is_not_omittable_tp,
    is_not_omitted,
    is_omittable_tp,
    is_omitted,
)
from retejo.markers.url_var import UrlVar, UrlVarMarker


@pytest.mark.parametrize(
    ("obj", "result"),
    [
        (Body[int], BodyMarker),
        (UrlVar[Omittable[int]], UrlVarMarker),  # type: ignore[misc]
        (Annotated[File[Omittable[int]], object()], FileMarker),  # type: ignore[misc]
    ],
)
def test_successful_get_marker(obj: Any, result: Any) -> None:
    assert isinstance(get_marker(obj), result)


@pytest.mark.parametrize(
    ("obj", "result"),
    [
        (Omittable[int], None),  # type: ignore[misc]
    ],
)
def test_unsuccessful_get_marker(obj: Any, result: Any) -> None:
    assert get_marker(obj) == result


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, False),
        ("Omitted", False),
        (Omitted(), True),
    ],
)
def test_is_omitted(value: Any, result: bool) -> None:
    assert is_omitted(value) is result


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, True),
        ("Omitted", True),
        (Omitted(), False),
    ],
)
def test_is_not_omitted(value: Any, result: bool) -> None:
    assert is_not_omitted(value) is result


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, False),
        (Omitted(), False),
        ("Omitted", True),
        (1, True),
    ],
)
def test_is_defined(value: Any, result: bool) -> None:
    assert is_defined(value) is result


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, True),
        (Omitted(), True),
        ("Omitted", False),
        (1, False),
    ],
)
def test_not_is_defined(value: Any, result: bool) -> None:
    assert is_not_defined(value) is result


@pytest.mark.parametrize(
    ("tp", "result"),
    [
        (Omittable[str], True),  # type: ignore[misc]
        (Omittable[str | int | None], True),  # type: ignore[misc]
        (Annotated[Omittable[str], object()], True),  # type: ignore[misc]
        (Annotated[Annotated[Omittable[str], object()], object()], True),  # type: ignore[misc]
    ],
)
def test_is_omittable_tp(tp: Any, result: bool) -> None:
    assert is_omittable_tp(tp) is result


@pytest.mark.parametrize(
    ("tp", "result"),
    [
        (Omittable[str], False),  # type: ignore[misc]
        (None, True),
        (Annotated[Annotated[Omittable[str], object()], object()], False),  # type: ignore[misc]
        (tuple[str, Omittable[int]], True),
    ],
)
def test_is_not_omittable_tp(tp: Any, result: bool) -> None:
    assert is_not_omittable_tp(tp) is result
