from abc import ABC
from typing import Any, Generic, TypeVar

from adaptix import Retort
from typing_extensions import override

from retejo.adaptix import method_dumper_provider, method_result_loader_provider
from retejo.adaptix.factory import AdaptixFactory
from retejo.client import BaseAsyncClient, BaseSyncClient
from retejo.http.entities.method import HttpMethod
from retejo.http.entities.request import HttpRequest
from retejo.http.entities.response import HttpResponse
from retejo.http.types import HttpMethodDumperType, HttpMethodResultLoaderType
from retejo.logger import DefaultLogger, Logger
from retejo.method_dumper import MethodDumper
from retejo.method_result_loader import MethodResultLoader

_RawResponseT = TypeVar("_RawResponseT")


_DEFAULT_METHOD_DUMPER: HttpMethodDumperType = MethodDumper(
    AdaptixFactory(
        Retort(
            recipe=[
                method_dumper_provider(),
            ],
        ),
    ),
)
_DEFAULT_METHOD_RESULT_LOADER: HttpMethodResultLoaderType[Any] = MethodResultLoader(
    AdaptixFactory(
        Retort(
            recipe=[
                method_result_loader_provider(),
            ],
        ),
    ),
)


class BaseSyncHttpClient(
    BaseSyncClient[
        HttpMethod[Any],
        HttpRequest,
        HttpResponse[_RawResponseT],
        _RawResponseT,
    ],
    Generic[_RawResponseT],
    ABC,
):
    __slots__ = (
        "_logger",
        "_method_dumper",
        "_method_result_loader",
    )

    def __init__(
        self,
        method_dumper: HttpMethodDumperType | None = None,
        method_result_loader: HttpMethodResultLoaderType[_RawResponseT] | None = None,
        logger: Logger | None = None,
    ) -> None:
        if logger is None:
            logger = DefaultLogger()

        if method_dumper is None:
            method_dumper = _DEFAULT_METHOD_DUMPER

        if method_result_loader is None:
            method_result_loader = _DEFAULT_METHOD_RESULT_LOADER

        self._logger = logger
        self._method_dumper = method_dumper
        self._method_result_loader = method_result_loader

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._method_dumper!r}, {self._method_result_loader!r}, {self._logger!r})>"

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def method_dumper(self) -> HttpMethodDumperType:
        return self._method_dumper

    @property
    def method_result_loader(
        self,
    ) -> HttpMethodResultLoaderType[_RawResponseT]:
        return self._method_result_loader


class BaseAsyncHttpClient(
    BaseAsyncClient[HttpMethod[Any], HttpRequest, HttpResponse[_RawResponseT], _RawResponseT],
    Generic[_RawResponseT],
    ABC,
):
    __slots__ = (
        "_logger",
        "_method_dumper",
        "_method_result_loader",
    )

    def __init__(
        self,
        method_dumper: HttpMethodDumperType | None = None,
        method_result_loader: HttpMethodResultLoaderType[_RawResponseT] | None = None,
        logger: Logger | None = None,
    ) -> None:
        if logger is None:
            logger = DefaultLogger()

        if method_dumper is None:
            method_dumper = _DEFAULT_METHOD_DUMPER

        if method_result_loader is None:
            method_result_loader = _DEFAULT_METHOD_RESULT_LOADER

        self._logger = logger
        self._method_dumper = method_dumper
        self._method_result_loader = method_result_loader

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._method_dumper!r}, {self._method_result_loader!r}, {self._logger!r})>"

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def method_dumper(self) -> HttpMethodDumperType:
        return self._method_dumper

    @property
    def method_result_loader(
        self,
    ) -> HttpMethodResultLoaderType[_RawResponseT]:
        return self._method_result_loader
