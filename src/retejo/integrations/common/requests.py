import urllib.parse
from collections.abc import Mapping
from json import JSONDecodeError
from typing import Any, override

from requests import RequestException, Session

from retejo.errors import ClientLibraryError, MalformedResponseError
from retejo.integrations.common.base import SyncBaseClient
from retejo.interfaces import Request, Response


class RequestsBaseClient(SyncBaseClient):
    _base_url: str
    _session: Session

    def __init__(
        self,
        base_url: str,
        session: Session | None = None,
        cookies: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__()

        self._base_url = base_url

        if session is None:
            self._session = Session()
        else:
            self._session = session

        if headers is not None:
            self._session.headers.update(headers)
        if cookies is not None:
            self._session.cookies.update(cookies)

    @override
    def send_request(
        self,
        request: Request,
    ) -> Response:
        response = self._session.request(
            method=request.http_method,
            url=urllib.parse.urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            headers=request.headers,
        )

        try:
            data = response.json()
        except RequestException as e:
            raise ClientLibraryError from e
        except JSONDecodeError as e:
            raise MalformedResponseError from e

        return Response(
            data=data,
            status_code=response.status_code,
        )

    @override
    def close(self) -> None:
        self._session.close()
