from abc import abstractmethod
from typing import Protocol, runtime_checkable

from retejo._internal.interfaces.sendable_method import AsyncSendableMethod, SyncSendableMethod
from retejo._internal.interfaces.sendable_request import (
    AsyncSendableRequest,
    Response,
    SyncSendableRequest,
)


@runtime_checkable
class SyncClient(
    SyncSendableRequest,
    SyncSendableMethod,
    Protocol,
):
    @abstractmethod
    def _handle_error_response(self, response: Response) -> None:
        raise NotImplementedError

    @abstractmethod
    def _handle_response(self, response: Response) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


@runtime_checkable
class AsyncClient(
    AsyncSendableRequest,
    AsyncSendableMethod,
    Protocol,
):
    @abstractmethod
    async def _handle_error_response(self, response: Response) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _handle_response(self, response: Response) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    async def aclose(self) -> None:
        await self.close()
