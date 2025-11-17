from collections.abc import Mapping

from typing_extensions import Any, override

from retejo.entities.request import Request
from retejo.entities.request_context_proxy import RequestContextProxy


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

    @override
    def __repr__(self) -> str:
        args = (
            repr(self._context),
            repr(self._url),
            repr(self._http_method),
            repr(self._body),
            repr(self._headers),
            repr(self._query_params),
            repr(self._form),
        )
        return f"<{self.__class__.__name__}{args}>"

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
