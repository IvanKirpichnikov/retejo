from abc import abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from retejo.interfaces.method import HTTPMethod, Method
from retejo.interfaces.request_conext_builder import RequestContextBuilder


@dataclass(slots=True, frozen=True)
class Request:
    url: str
    http_method: HTTPMethod
    body: Mapping[str, str] | None = None
    headers: Mapping[str, str] | None = None
    query_params: Mapping[str, str] | None = None


@dataclass(frozen=True, slots=True)
class Response:
    body: Mapping[str, Any]
    status_code: int


@runtime_checkable
class SendableMethod(Protocol):
    @abstractmethod
    def send_method[T](
        self,
        method: Method[T],
    ) -> T:
        raise NotImplementedError


@runtime_checkable
class Session(SendableMethod, Protocol):
    _request_context_builder: RequestContextBuilder

    __slots__ = ("_request_context_builder",)

    @abstractmethod
    def send_request(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError

    @abstractmethod
    def _handle_error_response(self, response: Response) -> None:
        raise NotImplementedError

    @abstractmethod
    def _handle_response(self, response: Response) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
