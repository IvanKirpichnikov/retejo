from typing import Any, Protocol, overload

__all__ = ["Factory"]


class Factory(Protocol):
    @overload
    def load[T](self, data: Any, tp: type[T], /) -> T: ...

    @overload
    def load(self, data: Any, tp: Any, /) -> Any: ...

    def load(self, data: Any, tp: Any, /) -> Any: ...

    @overload
    def dump[T](self, data: T, tp: type[T], /) -> Any: ...

    @overload
    def dump(self, data: Any, tp: Any | None = None, /) -> Any: ...

    def dump(self, data: Any, tp: Any | None = None, /) -> Any: ...
