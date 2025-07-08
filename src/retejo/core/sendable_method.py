from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

from retejo.core.entities import Method

_MethodResultT = TypeVar("_MethodResultT")
_MethodT_contra = TypeVar("_MethodT_contra", bound=Method, contravariant=True)


@runtime_checkable
class AsyncSendableMethod(Protocol[_MethodT_contra]):
    __slots__ = ()

    @abstractmethod
    async def send_method(
        self,
        method: _MethodT_contra,
    ) -> _MethodResultT:
        raise NotImplementedError

    @abstractmethod
    async def handle_method(self, method: _MethodT_contra) -> None:
        raise NotImplementedError


@runtime_checkable
class SyncSendableMethod(Protocol[_MethodT_contra]):
    __slots__ = ()

    @abstractmethod
    def send_method(
        self,
        method: _MethodT_contra,
    ) -> _MethodResultT:  # type: ignore[type-var] # A function returning TypeVar should receive at least one argument containing the same TypeVar
        raise NotImplementedError

    @abstractmethod
    def handle_method(self, method: _MethodT_contra) -> None:
        raise NotImplementedError
