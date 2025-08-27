from collections.abc import Mapping
from dataclasses import dataclass
from typing import IO, Any, ClassVar, Generic, TypeVar, TypedDict

from typing_extensions import Generic as GenericExtensions, TypeVar as TypeVarExtensions

from retejo.core.entities import AnyResult, Method, Request, RequestContextProxy, Response


class ResponseLoadData(TypedDict, total=True):
    data: Mapping[str, Any]
    headers: Mapping[str, Any]
    cookies: Mapping[str, Any]


@dataclass(slots=True, frozen=True)
class FileObj:
    contents: str | bytes | IO[bytes]
    content_type: str | None = None
    filename: str | None = None


class HttpRequest(Request):
    __slots__ = (
        "_body",
        "_form",
        "_headers",
        "_http_method",
        "_query_params",
        "_url",
    )

    def __init__(  # noqa: WPS211
        self,
        context: RequestContextProxy,
        url: str,
        http_method: str,
        body: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        query_params: Mapping[str, str] | None = None,
        form: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(context)
        self._url = url
        self._http_method = http_method
        self._body = body
        self._headers = headers
        self._query_params = query_params
        self._form = form

    @property
    def url(self) -> str:
        return self._url

    @property
    def http_method(self) -> str:
        return self._http_method

    @property
    def body(self) -> Mapping[str, str] | None:
        return self._body

    @property
    def headers(self) -> Mapping[str, str] | None:
        return self._headers

    @property
    def query_params(self) -> Mapping[str, str] | None:
        return self._query_params

    @property
    def form(self) -> Mapping[str, Any] | None:
        return self._form


_RawResponseT = TypeVar("_RawResponseT")


class HttpResponse(Response, Generic[_RawResponseT]):
    __slots__ = (
        "_cookies",
        "_data",
        "_headers",
        "_raw",
        "_status_code",
    )

    def __init__(
        self,
        data: Mapping[str, Any],
        headers: Mapping[str, Any],
        cookies: Mapping[str, Any],
        status_code: int,
        raw: _RawResponseT,
    ) -> None:
        super().__init__()
        self._data = data
        self._headers = headers
        self._cookies = cookies
        self._status_code = status_code
        self._raw = raw

    @property
    def data(self) -> Mapping[str, Any]:
        return self._data

    @property
    def headers(self) -> Mapping[str, Any]:
        return self._headers

    @property
    def cookies(self) -> Mapping[str, Any]:
        return self._cookies

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def raw(self) -> _RawResponseT:
        return self._raw


_MethodResultT = TypeVarExtensions("_MethodResultT", default=AnyResult)


class HttpMethod(Method[_MethodResultT], GenericExtensions[_MethodResultT]):
    __url__: ClassVar[str]
    __http_method__: ClassVar[str]
