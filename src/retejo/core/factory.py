from typing import Any, Protocol, TypeVar, overload

from adaptix import Retort
from typing_extensions import override

_Tp = TypeVar("_Tp")


class Factory(Protocol):
    __slots__ = ()

    @overload
    def load(self, data: Any, tp: type[_Tp], /) -> _Tp: ...

    @overload
    def load(self, data: Any, tp: Any, /) -> Any: ...

    def load(self, data: Any, tp: Any, /) -> Any: ...

    @overload
    def dump(self, data: _Tp, tp: type[_Tp], /) -> Any: ...

    @overload
    def dump(self, data: Any, tp: Any | None = None, /) -> Any: ...

    def dump(self, data: Any, tp: Any | None = None, /) -> Any: ...


class AdaptixFactory(Factory):
    __slots__ = ("_retort",)

    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    @override
    def load(self, data: Any, tp: Any, /) -> Any:
        return self._retort.load(data, tp)

    @override
    def dump(self, data: Any, tp: Any | None = None, /) -> Any:
        return self._retort.dump(data, tp)
