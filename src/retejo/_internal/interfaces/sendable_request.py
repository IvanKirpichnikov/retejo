from abc import abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from retejo._internal.interfaces.request_context_builder import RequestContext


@dataclass(slots=True, frozen=True)
class Request:
    url: str
    http_method: str
    context: RequestContext
    body: Mapping[str, str] | None = None
    headers: Mapping[str, str] | None = None
    query_params: Mapping[str, str] | None = None


@dataclass(frozen=True, slots=True)
class Response:
    data: Mapping[str, Any]
    status_code: int


@runtime_checkable
class AsyncSendableRequest(Protocol):
    @abstractmethod
    async def send_request(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError


@runtime_checkable
class SyncSendableRequest(Protocol):
    @abstractmethod
    def send_request(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError
