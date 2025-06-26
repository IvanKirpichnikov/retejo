from abc import abstractmethod
from collections.abc import Mapping
from typing import Any, Protocol, TypeAlias, runtime_checkable

from retejo.markers.base import BaseMarker
from retejo.method import Method

RequestContext: TypeAlias = Mapping[type[BaseMarker], Mapping[str, Any]]


@runtime_checkable
class RequestContextBuilder(Protocol):
    @abstractmethod
    def build(self, method: Method[Any]) -> RequestContext:
        raise NotImplementedError
