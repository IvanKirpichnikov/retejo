from typing import Any, Protocol, TypeVar, overload

_TypeHintT = TypeVar("_TypeHintT")


class Factory(Protocol):
    __slots__ = ()

    @overload
    def dump(self, data: _TypeHintT, type_hint: type[_TypeHintT]) -> Any: ...

    @overload
    def dump(self, data: Any, type_hint: Any | None = None) -> Any: ...

    def dump(self, data: Any, type_hint: Any | None = None) -> Any: ...

    @overload
    def load(self, data: Any, type_hint: type[_TypeHintT]) -> _TypeHintT: ...

    @overload
    def load(self, data: Any, type_hint: Any) -> Any: ...

    def load(self, data: Any, type_hint: Any) -> Any: ...
