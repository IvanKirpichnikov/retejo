from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, ClassVar, Generic, TypeVar

from typing_extensions import dataclass_transform

from retejo._type_tools.common import TypeHint
from retejo._type_tools.fundamentals import get_generic_args, strip_alias
from retejo.core.markers import BaseMarker
from retejo.utils.parents_resolver import ParentsResolver


class RequestContextProxy:
    def __init__(self, data: Mapping[Any, Any]) -> None:
        self._data = data

    def _make_key(self, key: str | type[BaseMarker]) -> str:
        return key if isinstance(key, str) else key.name

    def __getitem__(self, key: str | type[BaseMarker]) -> Any:
        return self._data[self._make_key(key)]

    def get(self, key: str | type[BaseMarker], default: Any | None = None) -> Any:
        return self._data.get(self._make_key(key), default)


_ClsT = TypeVar("_ClsT")


@dataclass_transform(kw_only_default=True)
def retejo_request(cls: type[_ClsT]) -> type[_ClsT]:
    return dataclass(
        slots=True,
        kw_only=True,
    )(cls)


@dataclass_transform(kw_only_default=True)
def retejo_response(cls: type[_ClsT]) -> type[_ClsT]:
    return dataclass(
        slots=True,
        kw_only=True,
    )(cls)


@retejo_request
class Request:
    """Base retejo request class."""

    context: RequestContextProxy


@retejo_response
class Response:
    """Base retejo response class."""


def get_generic_param(
    tp: TypeHint,
    module_name: str,
    parent_name: str,
    position_param: int,
    param_name: str,
) -> TypeHint:
    parents = ParentsResolver().get_parents(tp)
    for parent in parents:
        origin_tp = strip_alias(parent)
        if origin_tp.__name__ == parent_name and origin_tp.__module__ == module_name:
            return get_generic_args(parent)[position_param]

    raise RuntimeError(f"Not found type for {param_name!r} param by {tp!r}")


@dataclass_transform(frozen_default=True, kw_only_default=True)
class MethodMetaClass(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        class_: Any = super().__new__(cls, name, bases, namespace)

        try:
            class_ = dataclass(
                frozen=True,
                slots=True,
                kw_only=True,
            )(class_)
        except TypeError as e:
            # checking that an object has not been decorated with a dataclass
            if "Cannot overwrite attribute __setattr__ in class" not in e.args[0]:
                raise

        if class_.__name__ != "Method" or class_.__module__ != __name__:
            class_.__result__ = get_generic_param(
                tp=class_, module_name=__name__, parent_name="Method", position_param=0, param_name="__result__"
            )

        return class_


_MethodResultT = TypeVar("_MethodResultT")


class Method(Generic[_MethodResultT], metaclass=MethodMetaClass):
    __result__: ClassVar[type[_MethodResultT]]  # type: ignore[misc]
