from abc import abstractmethod
from types import TracebackType
from typing import Protocol, runtime_checkable

from typing_extensions import Self

from retejo.interfaces.sendable_method import AsyncSendableMethod, SyncSendableMethod
from retejo.interfaces.sendable_request import (
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

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


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

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
