from abc import abstractmethod
from types import TracebackType
from typing import Protocol, TypeVar, runtime_checkable

from typing_extensions import Self

from retejo.core.entities import Method, Request, Response
from retejo.core.sendable_method import AsyncSendableMethod, SyncSendableMethod
from retejo.core.sendable_request import AsyncSendableRequest, SyncSendableRequest

_ResponseT = TypeVar("_ResponseT", bound=Response)

_RequestT_contra = TypeVar("_RequestT_contra", bound=Request, contravariant=True)
_MethodT_contra = TypeVar("_MethodT_contra", bound=Method, contravariant=True)


@runtime_checkable
class SyncClient(
    SyncSendableMethod[_MethodT_contra],
    SyncSendableRequest[_RequestT_contra, _ResponseT],
    Protocol[_MethodT_contra, _RequestT_contra, _ResponseT],
):
    __slots__ = ()

    @abstractmethod
    def handle_response(self, response: _ResponseT) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_error_response(self, response: _ResponseT) -> None:
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
    AsyncSendableMethod[_MethodT_contra],
    AsyncSendableRequest[_RequestT_contra, _ResponseT],
    Protocol[_MethodT_contra, _RequestT_contra, _ResponseT],
):
    __slots__ = ()

    @abstractmethod
    async def handle_response(self, response: _ResponseT) -> None:
        raise NotImplementedError

    @abstractmethod
    async def handle_error_response(self, response: _ResponseT) -> None:
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
