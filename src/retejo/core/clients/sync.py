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
class SyncSendableMethod(Protocol[_MethodT_contra]):
    __slots__ = ()

    @abstractmethod
    def send_method(
        self,
        method: _MethodT_contra,
    ) -> _MethodResultT:  # type: ignore[type-var]
        """
        Send method.

        Responsible for sending the request and converting the response into a method result
        """
        raise NotImplementedError


@runtime_checkable
class SyncClient(
    SyncSendableMethod[_MethodT_contra],
    Protocol[_MethodT_contra, _RequestT_contra, _ResponseT],
):
    """
    Sync client.

    The chain of method calls in send_method
    |_ send_method
      |_ handle_method
      |_ handle_request
      |_ send_request
      |_ handle_response
      | |_ handle_error_response (Maybe)
    """

    __slots__ = ()

    @abstractmethod
    def handle_method(self, method: _MethodT_contra) -> None:
        raise NotImplementedError

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

    @abstractmethod
    def handle_error_response(self, response: _ResponseT) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError
