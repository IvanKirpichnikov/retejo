from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView
from typing import Any, TypeAlias, TypeVar, overload

from typing_extensions import override

from retejo.entities.marker import Marker

_DefaultT = TypeVar("_DefaultT")
_RequestContextKey: TypeAlias = str | type[Marker]


def _make_key(key: Any) -> Any:
    return key.marker_name if issubclass(key, Marker) else key


class RequestContextProxy(Mapping[_RequestContextKey, Any]):
    __slots__ = ("_request_context",)

    _request_context: Mapping[str, Any]

    def __init__(self, request_context: Mapping[str, Any]) -> None:
        self._request_context = request_context

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._request_context!r})>"

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._request_context)

    @override
    def __len__(self) -> int:
        return len(self._request_context)

    @override
    def __getitem__(self, key: _RequestContextKey) -> Any:
        return self._request_context[_make_key(key)]

    @overload
    def get(self, key: _RequestContextKey, /) -> Any | None: ...

    @overload
    def get(self, key: _RequestContextKey, /, default: _DefaultT) -> Any | _DefaultT: ...

    @override
    def get(self, key: _RequestContextKey, /, default: Any = None) -> Any:
        return self._request_context.get(_make_key(key), default)

    @override
    def items(self) -> ItemsView[str, Any]:
        return self._request_context.items()

    @override
    def keys(self) -> KeysView[str]:
        return self._request_context.keys()

    @override
    def values(self) -> ValuesView[Any]:
        return self._request_context.values()

    @override
    def __contains__(self, key: object, /) -> bool:
        return _make_key(key) in self._request_context

    @override
    def __eq__(self, other: object, /) -> bool:
        return self._request_context == other
