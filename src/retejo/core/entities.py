from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar, Final, Generic, TypeVar

from typing_extensions import dataclass_transform

from retejo._internal.type_tools.get_generic_param import get_generic_param
from retejo.core.markers import BaseMarker

_DATACLASS_FIELDS: Final = "__dataclass_fields__"


class RequestContextProxy:
    def __init__(self, request_context: Mapping[Any, Any]) -> None:
        self._request_context = request_context

    def __getitem__(self, key: str | type[BaseMarker]) -> Any:
        return self._request_context[self._make_key(key)]

    def get(self, key: str | type[BaseMarker], default: Any | None = None) -> Any:
        return self._request_context.get(self._make_key(key), default)

    def _make_key(self, key: str | type[BaseMarker]) -> str:
        return key if isinstance(key, str) else key.name


class Request:
    """Base retejo request class."""

    __slots__ = ("_context",)

    def __init__(self, context: RequestContextProxy) -> None:
        self._context = context

    @property
    def context(self) -> RequestContextProxy:
        return self._context


class Response:
    """Base retejo response class."""

    __slots__ = ()


_SequenceResultT = TypeVar("_SequenceResultT")


@dataclass(slots=True)
class SequenceResult(Generic[_SequenceResultT]):
    result: Sequence[_SequenceResultT]


class AnyResult:
    """
    Any result.

    Use if get raw data.
    """


@dataclass_transform(frozen_default=True, kw_only_default=True)
class MethodMetaClass(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> Any:
        class_: Any = super().__new__(cls, name, bases, namespace)

        # checking that an object has not been decorated with a dataclass
        if _DATACLASS_FIELDS in class_.__dict__:
            return class_

        class_ = dataclass(
            frozen=True,
            slots=True,
            kw_only=True,
        )(class_)

        if class_.__name__ != "Method" or class_.__module__ != __name__:
            class_.__result__ = get_generic_param(
                tp=class_,
                module_name=__name__,
                parent_name="Method",
                position_param=0,
                param_name="__result__",
            )

        return class_


_MethodResultT = TypeVar("_MethodResultT")


class Method(Generic[_MethodResultT], metaclass=MethodMetaClass):
    __result__: ClassVar[type[_MethodResultT]]  # type: ignore[misc]
