import urllib.parse
from collections.abc import Mapping
from json import JSONDecodeError
from typing import override

from requests import RequestException, Session

from retejo.errors import ClientLibraryError, MalformedResponseError
from retejo.integrations.base import SyncBaseClient
from retejo.interfaces.sendable_request import Request, Response


class RequestsClient(SyncBaseClient):
    _base_url: str
    _session: Session

    __slots__ = (
        "_base_url",
        "_session",
    )

    def __init__(
        self,
        base_url: str,
        session: Session | None = None,
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
            body = response.json()
        except RequestException as e:
            raise ClientLibraryError from e
        except JSONDecodeError as e:
            raise MalformedResponseError from e

        return Response(
            body=body,
            status_code=response.status_code,
        )

    @override
    def close(self) -> None:
        self._session.close()
