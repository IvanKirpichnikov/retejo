from abc import abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias, runtime_checkable

from retejo.file_obj import FileObj
from retejo.utils.request_context_proxy import RequestContextProxy

MarkerName: TypeAlias = str


@dataclass(slots=True, frozen=True)
class Request:
    url: str
    http_method: str
    context: RequestContextProxy
    body: Mapping[str, str] | None = None
    headers: Mapping[str, str] | None = None
    query_params: Mapping[str, str] | None = None
    files: Mapping[str, FileObj] | None = None


@dataclass(frozen=True, slots=True)
class Response:
    data: Mapping[str, Any]
    status_code: int


@runtime_checkable
class AsyncSendableRequest(Protocol):
    __slots__ = ()

    @abstractmethod
    async def send_request(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError

    @abstractmethod
    async def do_request(
        self,
        request: Request,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def do_response(
        self,
        response: Response,
    ) -> None:
        raise NotImplementedError


@runtime_checkable
class SyncSendableRequest(Protocol):
    __slots__ = ()

    @abstractmethod
    def send_request(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError

    @abstractmethod
    def do_request(
        self,
        request: Request,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def do_response(
        self,
        response: Response,
    ) -> None:
        raise NotImplementedError
