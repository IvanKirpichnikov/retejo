from abc import abstractmethod
from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from retejo._internal.markers.base import BaseMarker
from retejo.method import Method

type RequestContext = Mapping[type[BaseMarker], Mapping[str, Any]]


@runtime_checkable
class RequestContextBuilder(Protocol):
    @abstractmethod
    def build(self, method: Method[Any]) -> RequestContext:
        raise NotImplementedError
