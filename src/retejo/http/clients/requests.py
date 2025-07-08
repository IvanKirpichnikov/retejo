import urllib.parse
from collections.abc import Mapping, MutableMapping
from json import JSONDecodeError
from typing import IO, Any, cast

from requests import RequestException, Response, Session

from retejo.core.errors import IntegrationError
from retejo.http.clients.base import SyncHttpClient
from retejo.http.entities import FileObj, HttpRequest, HttpResponse
from retejo.http.errors import MalformedResponseError


class RequestsClient(SyncHttpClient[Response]):
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
            session_cookies: MutableMapping[Any, Any] = self._session.cookies
            session_cookies.update(cookies)

    def send_request(
        self,
        request: HttpRequest,
    ) -> HttpResponse[Response]:
        if request.files is not None:
            files = {file_key: self.file_obj_converter(file_key, file) for file_key, file in request.files.items()}
        else:
            files = None

        response = self._session.request(
            method=request.http_method,
            url=urllib.parse.urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            files=files,
            headers=request.headers,
        )
        data = self.retrieve_response_data(response)

        return HttpResponse(
            data=data,
            status_code=response.status_code,
            raw=response,
        )

    def file_obj_converter(
        self,
        file_key: str,
        file: FileObj,
    ) -> tuple[str, str | IO[bytes], str]:
        return (
            file.filename or file_key,
            file.contents,
            cast("str", file.content_type),
        )

    def retrieve_response_data(self, raw_response: Response) -> Any:
        try:
            return raw_response.json()
        except RequestException as e:
            raise IntegrationError from e
        except JSONDecodeError as e:
            raise MalformedResponseError from e

    def close(self) -> None:
        self._session.close()
