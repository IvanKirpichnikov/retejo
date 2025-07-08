from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

from retejo.core.entities import Request, Response

_ResponseT = TypeVar("_ResponseT", bound=Response)
_RequestT_contra = TypeVar("_RequestT_contra", bound=Request, contravariant=True)


@runtime_checkable
class AsyncSendableRequest(Protocol[_RequestT_contra, _ResponseT]):
    __slots__ = ()

    @abstractmethod
    async def send_request(
        self,
        request: _RequestT_contra,
    ) -> _ResponseT:
        raise NotImplementedError

    @abstractmethod
    async def handle_request(
        self,
        request: _RequestT_contra,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def handle_response(
        self,
        response: _ResponseT,
    ) -> None:
        raise NotImplementedError


@runtime_checkable
class SyncSendableRequest(Protocol[_RequestT_contra, _ResponseT]):
    __slots__ = ()

    @abstractmethod
    def send_request(
        self,
        request: _RequestT_contra,
    ) -> _ResponseT:
        raise NotImplementedError

    @abstractmethod
    def handle_request(
        self,
        request: _RequestT_contra,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_response(
        self,
        response: _ResponseT,
    ) -> None:
        raise NotImplementedError
