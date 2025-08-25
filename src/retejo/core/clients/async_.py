# flake8: noqa: WPS102
from abc import abstractmethod
from types import TracebackType
from typing import Any, Protocol, TypeVar, runtime_checkable

from typing_extensions import Self

from retejo.core.entities import Method, Request, Response

_MethodResultT = TypeVar("_MethodResultT")
_MethodT_contra = TypeVar("_MethodT_contra", bound=Method[Any], contravariant=True)

_ResponseT = TypeVar("_ResponseT", bound=Response)
_RequestT_contra = TypeVar("_RequestT_contra", bound=Request, contravariant=True)


@runtime_checkable
class AsyncSendableMethod(Protocol[_MethodT_contra]):
    __slots__ = ()

    @abstractmethod
    async def send_method(
        self,
        method: _MethodT_contra,
    ) -> _MethodResultT:
        """
        Send method.

        Responsible for sending the request and converting the response into a method result
        """
        raise NotImplementedError


@runtime_checkable
class AsyncClient(
    AsyncSendableMethod[_MethodT_contra],
    Protocol[_MethodT_contra, _RequestT_contra, _ResponseT],
):
    __slots__ = ()

    """
    Async client

    The chain of method calls in send_method
    |_ send_method
      |_ handle_method
      |_ method_converter
      |_ handle_request
      |_ send_request
      |_ handle_response
      | |_ handle_error_response (Maybe)
      |_ method_result_converter
    """
    __slots__ = ()

    @abstractmethod
    async def handle_method(self, method: _MethodT_contra) -> None:
        raise NotImplementedError

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

    @abstractmethod
    async def handle_error_response(self, response: _ResponseT) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def aclose(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError
