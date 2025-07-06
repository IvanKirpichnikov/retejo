from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

from retejo.method import Method

T = TypeVar("T")


@runtime_checkable
class AsyncSendableMethod(Protocol):
    __slots__ = ()

    @abstractmethod
    async def send_method(
        self,
        method: Method[T],
    ) -> T:
        raise NotImplementedError

    @abstractmethod
    async def do_method(self, method: Method[T]) -> None:
        raise NotImplementedError


@runtime_checkable
class SyncSendableMethod(Protocol):
    __slots__ = ()

    @abstractmethod
    def send_method(
        self,
        method: Method[T],
    ) -> T:
        raise NotImplementedError

    @abstractmethod
    def do_method(self, method: Method[T]) -> None:
        raise NotImplementedError
