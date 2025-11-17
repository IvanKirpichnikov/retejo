from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Generic, Sequence, TypeVar

from typing_extensions import Self

from retejo.entities.method import Method
from retejo.entities.request import Request
from retejo.entities.response import Response
from retejo.interfaces.method_caller import AsyncMethodCaller, SyncMethodCaller
from retejo.interfaces.method_caller_factory import MethodCallerFactory

_MethodT = TypeVar("_MethodT", bound=Method[Any])
_RequestT_contra = TypeVar("_RequestT_contra", bound=Request, contravariant=True)
_ResponseT = TypeVar("_ResponseT", bound=Response[Any])
_RawResponseT = TypeVar("_RawResponseT")


class AsyncClient(
    Generic[
        _MethodT,
        _RequestT_contra,
        _ResponseT,
        _RawResponseT,
    ],
    ABC,
):
    __slots__ = ()

    @classmethod
    @abstractmethod
    def register_method(cls, method_cls: type[Method[Any]]) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_registred_methods(cls) -> Sequence[type[Method[Any]]]:
        raise NotImplementedError

    @abstractmethod
    def get_method_caller_factory(
        self,
    ) -> MethodCallerFactory[
        Self,
        _MethodT,
        AsyncMethodCaller[Any, Any],
    ]:
        raise NotImplementedError

    @abstractmethod
    async def send_request(
        self,
        request: _RequestT_contra,
    ) -> _ResponseT:
        raise NotImplementedError

    @abstractmethod
    async def retrieve_response_body(self, raw_response: _RawResponseT) -> Any:
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


class SyncClient(
    Generic[
        _MethodT,
        _RequestT_contra,
        _ResponseT,
        _RawResponseT,
    ],
    ABC,
):
    __slots__ = ()

    @classmethod
    @abstractmethod
    def register_method(cls, method_cls: type[Method[Any]]) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_registred_methods(cls) -> Sequence[type[Method[Any]]]:
        raise NotImplementedError

    @abstractmethod
    def get_method_caller_factory(
        self,
    ) -> MethodCallerFactory[Self, _MethodT, SyncMethodCaller[Any, Any]]:
        raise NotImplementedError

    @abstractmethod
    def send_request(
        self,
        request: _RequestT_contra,
    ) -> _ResponseT:
        raise NotImplementedError

    @abstractmethod
    def retrieve_response_body(self, raw_response: _RawResponseT) -> Any:
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
