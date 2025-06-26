from typing import Any, Protocol, TypeVar, overload, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class Factory(Protocol):
    @overload
    def load(self, data: Any, tp: type[T], /) -> T: ...

    @overload
    def load(self, data: Any, tp: Any, /) -> Any: ...

    def load(self, data: Any, tp: Any, /) -> Any: ...

    @overload
    def dump(self, data: T, tp: type[T], /) -> Any: ...

    @overload
    def dump(self, data: Any, tp: Any | None = None, /) -> Any: ...

    def dump(self, data: Any, tp: Any | None = None, /) -> Any: ...
