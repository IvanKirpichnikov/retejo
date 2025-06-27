from typing import Annotated, Any

import pytest

from retejo.markers.omitted import (
    Omittable,
    Omitted,
    is_defined,
    is_not_defined,
    is_not_omittable,
    is_not_omitted,
    is_omittable,
    is_omitted,
)


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, False),
        ("Omitted", False),
        (Omitted(object), True),
    ],
)
def test_is_omitted(value: Any, result: bool) -> None:
    assert is_omitted(value) is result


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, True),
        ("Omitted", True),
        (Omitted(object), False),
    ],
)
def test_is_not_omitted(value: Any, result: bool) -> None:
    assert is_not_omitted(value) is result


@pytest.mark.parametrize(
    ("value", "result"),
    [
        (None, False),
        (Omitted(object), False),
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
        (Omitted(object), True),
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
def test_is_omittable(tp: Any, result: bool) -> None:
    assert is_omittable(tp) is result


@pytest.mark.parametrize(
    ("tp", "result"),
    [
        (Omittable[str], False),  # type: ignore[misc]
        (Annotated[Annotated[Omittable[str], object()], object()], False),  # type: ignore[misc]
        (None, True),
        (tuple[str, Omittable[int]], True),
    ],
)
def test_is_not_omittable(tp: Any, result: bool) -> None:
    assert is_not_omittable(tp) is result
