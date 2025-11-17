from abc import ABC
from typing import Any, Generic, TypeVar

from typing_extensions import override

from retejo.entities.method import Method
from retejo.entities.request import Request
from retejo.entities.response import Response
from retejo.interfaces.client import AsyncClient, SyncClient
from retejo.interfaces.method_caller import AsyncMethodCaller, SyncMethodCaller
from retejo.interfaces.method_caller_factory import MethodCallerFactory
from retejo.method_dumper import MethodDumper
from retejo.method_result_loader import MethodResultLoader

_ClientT = TypeVar(
    "_ClientT",
    bound=AsyncClient[Any, Any, Any, Any] | SyncClient[Any, Any, Any, Any],
)
_MethodT = TypeVar("_MethodT", bound=Method[Any])
_RequestT = TypeVar("_RequestT", bound=Request)
_ResponseT = TypeVar("_ResponseT", bound=Response[Any])
_MethodCallerT = TypeVar(
    "_MethodCallerT",
    bound=AsyncMethodCaller[Any, Any] | SyncMethodCaller[Any, Any],
)


class BaseMethodCallerFactory(
    MethodCallerFactory[
        _ClientT,
        _MethodT,
        _MethodCallerT,
    ],
    Generic[
        _ClientT,
        _MethodT,
        _RequestT,
        _ResponseT,
        _MethodCallerT,
    ],
    ABC,
):
    __slots__ = (
        "_method_dumper",
        "_method_result_loader",
    )

    def __init__(
        self,
        method_dumper: MethodDumper[_MethodT] | None = None,
        method_result_loader: MethodResultLoader[_MethodT, _RequestT, _ResponseT] | None = None,
    ) -> None:
        self._method_dumper = method_dumper
        self._method_result_loader = method_result_loader

    @override
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}({self._method_dumper!r}, {self._method_result_loader!r})>"
        )
