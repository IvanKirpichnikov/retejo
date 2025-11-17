from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from typing_extensions import override

from retejo.entities.response import Response

_RawResponseT = TypeVar("_RawResponseT")


class HttpResponse(Response[_RawResponseT], Generic[_RawResponseT]):
    __slots__ = (
        "_body",
        "_cookies",
        "_headers",
        "_status_code",
    )

    def __init__(
        self,
        body: Mapping[str, Any],
        headers: Mapping[str, Any],
        cookies: Mapping[str, Any],
        status_code: int,
        raw_response: _RawResponseT,
    ) -> None:
        super().__init__(raw_response)
        self._body = body
        self._headers = headers
        self._cookies = cookies
        self._status_code = status_code

    @override
    def __repr__(self) -> str:
        args = (
            repr(self._body),
            repr(self._headers),
            repr(self._cookies),
            repr(self._status_code),
            repr(self._raw_response),
        )
        return f"<{self.__class__.__name__}{args}>"

    @property
    @override
    def raw_result(self) -> Any:
        return self.body

    @property
    def body(self) -> Mapping[str, Any]:
        return self._body

    @property
    def headers(self) -> Mapping[str, Any]:
        return self._headers

    @property
    def cookies(self) -> Mapping[str, Any]:
        return self._cookies

    @property
    def status_code(self) -> int:
        return self._status_code
