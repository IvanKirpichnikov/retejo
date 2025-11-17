from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from retejo.entities.method import Method
from retejo.interfaces.method_caller import AsyncMethodCaller, SyncMethodCaller

if TYPE_CHECKING:
    from retejo.interfaces.client import AsyncClient, SyncClient

_ClientT_contra = TypeVar(
    "_ClientT_contra",
    contravariant=True,
    bound="AsyncClient[Any, Any, Any, Any] | SyncClient[Any, Any, Any, Any]",
)
_MethodT_contra = TypeVar(
    "_MethodT_contra",
    contravariant=True,
    bound=Method[Any],
)
_MethodCallerT_co = TypeVar(
    "_MethodCallerT_co",
    covariant=True,
    bound=AsyncMethodCaller[Any, Any] | SyncMethodCaller[Any, Any],
)


class MethodCallerFactory(
    Protocol[
        _ClientT_contra,
        _MethodT_contra,
        _MethodCallerT_co,
    ],
):
    __slots__ = ()

    @abstractmethod
    def __call__(
        self,
        client: _ClientT_contra,
        method_cls: type[_MethodT_contra],
    ) -> _MethodCallerT_co:
        raise NotImplementedError
