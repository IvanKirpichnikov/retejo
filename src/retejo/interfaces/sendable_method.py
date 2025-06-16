from abc import abstractmethod
from typing import Protocol, runtime_checkable

from retejo.interfaces.method import Method

__all__ = [
    "AsyncSendableMethod",
    "SyncSendableMethod",
]


@runtime_checkable
class AsyncSendableMethod(Protocol):
    @abstractmethod
    async def send_method[T](
        self,
        method: Method[T],
    ) -> T:
        raise NotImplementedError


@runtime_checkable
class SyncSendableMethod(Protocol):
    @abstractmethod
    def send_method[T](
        self,
        method: Method[T],
    ) -> T:
        raise NotImplementedError
