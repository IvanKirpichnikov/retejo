from abc import abstractmethod
from typing import Any, Generic, ParamSpec, TypeVar

_MethodResultT = TypeVar("_MethodResultT")
_MethodParamSpec = ParamSpec("_MethodParamSpec")


class SyncMethodCaller(Generic[_MethodParamSpec, _MethodResultT]):
    __slots__ = ()

    @property
    @abstractmethod
    def method_cls(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __call__(
        self,
        *args: _MethodParamSpec.args,
        **kwargs: _MethodParamSpec.kwargs,
    ) -> _MethodResultT:
        raise NotImplementedError


class AsyncMethodCaller(Generic[_MethodParamSpec, _MethodResultT]):
    __slots__ = ()

    @property
    @abstractmethod
    def method_cls(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def __call__(
        self,
        *args: _MethodParamSpec.args,
        **kwargs: _MethodParamSpec.kwargs,
    ) -> _MethodResultT:
        raise NotImplementedError
