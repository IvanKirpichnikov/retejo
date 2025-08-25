from json import JSONDecodeError
from typing import IO, Any, cast
from urllib.parse import urljoin

from requests import RequestException, Response, Session
from typing_extensions import override

from retejo.core.errors import IntegrationError
from retejo.http.clients.sync import SyncHttpClient
from retejo.http.entities import FileObj, HttpRequest, HttpResponse
from retejo.http.errors import MalformedResponseError
from retejo.http.logger_state import HttpLoggerState


class RequestsClient(SyncHttpClient[Response]):
    def __init__(
        self,
        base_url: str = "",
        session: Session | None = None,
        logger_state: HttpLoggerState | None = None,
    ) -> None:
        if logger_state is None:
            logger_state = HttpLoggerState()

        super().__init__(logger_state)

        self._base_url = base_url

        if session is None:
            self._session = Session()
        else:
            self._session = session

    @override
    def send_request(
        self,
        request: HttpRequest,
    ) -> HttpResponse[Response]:
        if request.form is not None:  # noqa: WPS504
            data = {}
            for key, value in request.form.items():
                if isinstance(value, FileObj):
                    data[key] = self.file_obj_converter(key, value)
                else:
                    data[key] = value

        else:
            data = None

        response = self._session.request(
            method=request.http_method,
            url=urljoin(self._base_url, request.url),
            params=request.query_params,
            json=request.body,
            data=data,
            headers=request.headers,
        )
        response_data = self.retrieve_response_data(response)

        return HttpResponse(
            data=response_data,
            headers=response.headers,
            cookies=response.cookies,
            status_code=response.status_code,
            raw=response,
        )

    def file_obj_converter(
        self,
        file_key: str,
        file_obj: FileObj,
    ) -> tuple[str, str | bytes | IO[bytes], str]:
        return (
            file_obj.filename or file_key,
            file_obj.contents,
            cast("str", file_obj.content_type),
        )

    @override
    def retrieve_response_data(self, raw_response: Response) -> Any:
        try:
            return raw_response.json()
        except RequestException as error:
            raise IntegrationError from error
        except JSONDecodeError as error:
            raise MalformedResponseError from error

    @override
    def close(self) -> None:
        self._session.close()
