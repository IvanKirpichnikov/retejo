from typing import Any, TypeVar, overload

from adaptix import Retort
from typing_extensions import override

from retejo.interfaces.factory import Factory

_TypeHintT = TypeVar("_TypeHintT")


class AdaptixFactory(Factory):
    __slots__ = ("_retort",)

    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._retort!r})"

    @property
    def retort(self) -> Retort:
        return self._retort

    @overload
    def load(self, data: Any, type_hint: type[_TypeHintT]) -> _TypeHintT: ...

    @overload
    def load(self, data: Any, type_hint: Any) -> Any: ...

    @override
    def load(self, data: Any, type_hint: Any) -> Any:
        return self._retort.load(data, type_hint)

    @overload
    def dump(self, data: _TypeHintT, type_hint: type[_TypeHintT]) -> Any: ...

    @overload
    def dump(self, data: Any, type_hint: Any | None = None) -> Any: ...

    @override
    def dump(self, data: Any, type_hint: Any | None = None) -> Any:
        return self._retort.dump(data, type_hint)
