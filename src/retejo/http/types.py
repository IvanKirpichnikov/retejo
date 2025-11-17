from typing import Any, TypeAlias, TypeVar

from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.method_dumper import MethodDumper
from retejo.method_result_loader import MethodResultLoader

_RawResponseT = TypeVar("_RawResponseT")

HttpMethodResultLoaderType: TypeAlias = MethodResultLoader[
    HttpMethod[Any],
    HttpRequest,
    HttpResponse[_RawResponseT],
]
HttpMethodDumperType: TypeAlias = MethodDumper[HttpMethod[Any]]
