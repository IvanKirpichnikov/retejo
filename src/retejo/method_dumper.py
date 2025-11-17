from typing import Any, Generic, TypeVar

from typing_extensions import override

from retejo.entities.method import Method
from retejo.interfaces.factory import Factory

_MethodT = TypeVar("_MethodT", bound=Method[Any])


class MethodDumper(Generic[_MethodT]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Factory) -> None:
        self._factory = factory

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._factory})>"

    @property
    def factory(self) -> Factory:
        return self._factory

    def dump(self, method: _MethodT) -> Any:
        return self._factory.dump(method)
