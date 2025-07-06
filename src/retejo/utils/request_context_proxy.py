from collections.abc import Mapping
from typing import Any, TypeAlias

from retejo.markers.base import BaseMarker

_Key: TypeAlias = str | type[BaseMarker]


class RequestContextProxy:
    def __init__(self, data: Mapping[Any, Any]) -> None:
        self._data = data

    def _make_key(self, key: _Key) -> str:
        return key if isinstance(key, str) else key.name

    def __getitem__(self, key: _Key) -> Any:
        return self._data[self._make_key(key)]

    def get(self, key: _Key, default: Any | None = None) -> Any:
        return self._data.get(self._make_key(key), default)
