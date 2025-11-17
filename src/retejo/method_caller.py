from abc import abstractmethod
from typing import Any, Generic, ParamSpec, TypeVar

from typing_extensions import override

from retejo.entities.method import Method
from retejo.entities.request import Request
from retejo.entities.response import Response
from retejo.interfaces.client import AsyncClient, SyncClient
from retejo.interfaces.method_caller import AsyncMethodCaller, SyncMethodCaller
from retejo.method_dumper import MethodDumper
from retejo.method_result_loader import MethodResultLoader

_MethodT = TypeVar("_MethodT", bound=Method[Any])
_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")
_RequestT = TypeVar("_RequestT", bound=Request)
_ResponseT = TypeVar("_ResponseT", bound=Response[Any])


class BaseSyncMethodCaller(
    SyncMethodCaller[_MethodParamSpec, _MethodResultT],
    Generic[
        _RequestT,
        _ResponseT,
        _MethodT,
        _MethodParamSpec,
        _MethodResultT,
    ],
):
    __slots__ = (
        "_client",
        "_method_cls",
        "_method_dumper",
        "_method_result_loader",
    )

    def __init__(
        self,
        method_cls: Any,
        client: SyncClient[Any, _RequestT, _ResponseT, Any],
        method_dumper: MethodDumper[_MethodT],
        method_result_loader: MethodResultLoader[_MethodT, _RequestT, _ResponseT],
    ) -> None:
        self._client = client
        self._method_cls = method_cls
        self._method_dumper = method_dumper
        self._method_result_loader = method_result_loader

    @override
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"{self._method_cls!r}, "
            f"{self._client!r}, "
            f"{self._method_dumper!r}, "
            f"{self._method_result_loader!r})>"
        )

    @property
    @override
    def method_cls(self) -> Any:
        return self._method_cls

    @override
    def __call__(
        self,
        *args: _MethodParamSpec.args,
        **kwargs: _MethodParamSpec.kwargs,
    ) -> _MethodResultT:
        method = self._method_cls(*args, **kwargs)
        self.prepare_method(method)

        request = self.method_to_request(method)
        self.prepare_request(request)

        response = self._client.send_request(request)
        if self.is_error_response(response):
            self.prepare_error_response(response)
        else:
            self.prepare_response(response)

        return self.load_method_result(method, request, response)

    def prepare_method(self, method: Any) -> None:
        return None

    @abstractmethod
    def method_to_request(self, method: _MethodT) -> _RequestT:
        raise NotImplementedError

    def prepare_request(self, request: _RequestT) -> None:
        return None

    def prepare_response(self, response: _ResponseT) -> None:
        return None

    @abstractmethod
    def is_error_response(self, response: _ResponseT) -> bool:
        raise NotImplementedError

    def prepare_error_response(self, response: _ResponseT) -> None:
        return None

    @abstractmethod
    def load_method_result(
        self,
        method: _MethodT,
        request: _RequestT,
        response: _ResponseT,
    ) -> _MethodResultT:
        raise NotImplementedError


class BaseAsyncMethodCaller(
    AsyncMethodCaller[_MethodParamSpec, _MethodResultT],
    Generic[
        _RequestT,
        _ResponseT,
        _MethodT,
        _MethodParamSpec,
        _MethodResultT,
    ],
):
    __slots__ = (
        "_client",
        "_method_cls",
        "_method_dumper",
        "_method_result_loader",
    )

    def __init__(
        self,
        method_cls: Any,
        client: AsyncClient[Any, _RequestT, _ResponseT, Any],
        method_dumper: MethodDumper[_MethodT],
        method_result_loader: MethodResultLoader[_MethodT, _RequestT, _ResponseT],
    ) -> None:
        self._client = client
        self._method_cls = method_cls
        self._method_dumper = method_dumper
        self._method_result_loader = method_result_loader

    @override
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"{self._method_cls!r}, "
            f"{self._client!r}, "
            f"{self._method_dumper!r}, "
            f"{self._method_result_loader!r})>"
        )

    @property
    @override
    def method_cls(self) -> Any:
        return self._method_cls

    @override
    async def __call__(
        self,
        *args: _MethodParamSpec.args,
        **kwargs: _MethodParamSpec.kwargs,
    ) -> _MethodResultT:
        method = self._method_cls(*args, **kwargs)
        await self.prepare_method(method)

        request = await self.method_to_request(method)
        await self.prepare_request(request)

        response = await self._client.send_request(request)
        if await self.is_error_response(response):
            await self.prepare_error_response(response)
        else:
            await self.prepare_response(response)

        return await self.load_method_result(method, request, response)

    async def prepare_method(self, method: Any) -> None:
        return None

    @abstractmethod
    async def method_to_request(self, method: _MethodT) -> _RequestT:
        raise NotImplementedError

    async def prepare_request(self, request: _RequestT) -> None:
        return None

    async def prepare_response(self, response: _ResponseT) -> None:
        return None

    @abstractmethod
    async def is_error_response(self, response: _ResponseT) -> bool:
        raise NotImplementedError

    async def prepare_error_response(self, response: _ResponseT) -> None:
        return None

    @abstractmethod
    async def load_method_result(
        self,
        method: _MethodT,
        request: _RequestT,
        response: _ResponseT,
    ) -> _MethodResultT:
        raise NotImplementedError
