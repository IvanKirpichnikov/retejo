from typing import IO, Any, TypeAlias, cast
from urllib.parse import urljoin

from requests import JSONDecodeError as RequestsJSONDecodeError, RequestException, Response, Session
from typing_extensions import Self, override

from retejo.entities.file_obj import FileObj
from retejo.error import IntegrationError
from retejo.http.clients import BaseSyncHttpClient
from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.errors import MalformedResponseError
from retejo.http.integrations.requests.method_caller_factory import RequestsMethodCallerFactory
from retejo.http.types import HttpMethodDumperType, HttpMethodResultLoaderType
from retejo.interfaces.method_caller import SyncMethodCaller
from retejo.interfaces.method_caller_factory import MethodCallerFactory
from retejo.logger import Logger

FileName: TypeAlias = str
FileContents: TypeAlias = str | bytes | IO[bytes]
ContentType: TypeAlias = str
FileObjTypeHint: TypeAlias = tuple[FileName, FileContents, ContentType]


class RequestsClient(BaseSyncHttpClient[Response]):
    __slots__ = (
        "_base_url",
        "_session",
    )

    def __init__(
        self,
        base_url: str = "",
        method_dumper: HttpMethodDumperType | None = None,
        method_result_loader: HttpMethodResultLoaderType[Response] | None = None,
        logger: Logger | None = None,
        session: Session | None = None,
    ) -> None:
        super().__init__(
            method_dumper=method_dumper,
            method_result_loader=method_result_loader,
            logger=logger,
        )

        self._base_url = base_url

        if session is None:
            session = Session()

        self._session = session

    @override
    def __repr__(self) -> str:
        args = (
            repr(self._base_url),
            repr(self._method_dumper),
            repr(self._method_result_loader),
            repr(self._logger),
        )
        return f"<{self.__class__.__name__}{args}>"

    @override
    def get_method_caller_factory(
        self,
    ) -> MethodCallerFactory[Self, HttpMethod[Any], SyncMethodCaller[Any, Any]]:
        return RequestsMethodCallerFactory(
            method_dumper=self._method_dumper,
            method_result_loader=self._method_result_loader,
        )

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
        response_data = self.retrieve_response_body(response)

        return HttpResponse(
            body=response_data,
            headers=response.headers,
            cookies=response.cookies,
            status_code=response.status_code,
            raw_response=response,
        )

    @override
    def retrieve_response_body(self, raw_response: Response) -> Any:
        try:
            return raw_response.json()
        except RequestsJSONDecodeError as error:
            raise MalformedResponseError from error
        except RequestException as error:
            raise IntegrationError from error

    def file_obj_converter(
        self,
        file_key: str,
        file_obj: FileObj,
    ) -> FileObjTypeHint:
        return (
            file_obj.filename or file_key,
            file_obj.contents,
            cast("str", file_obj.content_type),
        )

    @override
    def close(self) -> None:
        self._session.close()
