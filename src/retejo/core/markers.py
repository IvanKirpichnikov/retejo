from abc import ABC
from typing import (
    ClassVar,
    Literal,
    TypeAlias,
    TypeVar,
)

from typing_extensions import override


class BaseMarker(ABC):
    __slots__ = ()

    name: ClassVar[str]

    @override
    def __repr__(self) -> str:
        return f"<Marker {self.name!r}>"


class Omitted:
    __slots__ = ()

    def __bool__(self) -> Literal[False]:
        return False

    @override
    def __repr__(self) -> str:
        return "<Omitted>"


_OmittedValueT = TypeVar("_OmittedValueT")
Omittable: TypeAlias = _OmittedValueT | Omitted
