from collections.abc import Mapping
from dataclasses import dataclass
from typing import IO, Any, ClassVar, Generic, TypeVar

from retejo.core.entities import Method, Request, Response, retejo_request, retejo_response


@dataclass(slots=True, frozen=True)
class FileObj:
    contents: str | bytes | IO[bytes]
    content_type: str | None = None
    filename: str | None = None


@retejo_request
class HttpRequest(Request):
    url: str
    http_method: str
    body: Mapping[str, str] | None = None
    headers: Mapping[str, str] | None = None
    query_params: Mapping[str, str] | None = None
    form: Mapping[str, Any] | None = None


_RawResponseT = TypeVar("_RawResponseT")


@retejo_response
class HttpResponse(Response, Generic[_RawResponseT]):
    data: Mapping[str, Any]
    status_code: int
    raw: _RawResponseT


_MethodResultT = TypeVar("_MethodResultT")


class HttpMethod(Method[_MethodResultT], Generic[_MethodResultT]):
    __url__: ClassVar[str]
    __http_method__: ClassVar[str]
