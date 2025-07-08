from typing import Annotated, Any

import pytest

from retejo.core.markers import Omittable, get_marker
from retejo.http.markers import Body, BodyMarker, File, FileMarker, UrlVar, UrlVarMarker


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
