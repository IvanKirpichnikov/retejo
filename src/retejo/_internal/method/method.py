from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, dataclass_transform, get_args, get_origin

from retejo._internal.method.context import MethodContext, create_method_context
from retejo._internal.parents_resolver import ParentsResolver


def get_returning_tp(tp: Any) -> Any:
    parents = ParentsResolver().get_parents(tp)

    for parent in parents:
        if get_origin(parent) is Method:  # type: ignore[comparison-overlap]
            return get_args(parent)[0]

    raise RuntimeError(f"Not found __returning__ type by {tp!r} type")


@dataclass_transform(frozen_default=True)
class MethodMetaClass(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        klass: Any = type.__new__(cls, name, bases, namespace)

        if klass.__name__ == "Method":
            return klass

        klass = dataclass(frozen=True)(klass)

        klass.__returning__ = get_returning_tp(klass)
        klass.__context__ = create_method_context(klass)

        return klass


class Method[T](metaclass=MethodMetaClass):
    @property
    @abstractmethod
    def __url__(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def __method__(self) -> str:
        raise NotImplementedError

    # fill in meta class
    @property
    def __returning__(self) -> type[T]:
        raise NotImplementedError

    @property
    def __context__(self) -> MethodContext:
        raise NotImplementedError
