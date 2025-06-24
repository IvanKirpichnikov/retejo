from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, dataclass_transform, get_args, get_origin

from retejo._internal.parents_resolver import ParentsResolver
from retejo.method.context import MethodContext, create_method_context


def get_returning_tp(tp: Any) -> Any:
    parents = ParentsResolver().get_parents(tp)

    for parent in parents:
        if get_origin(parent) is Method:  # type: ignore[comparison-overlap]
            return get_args(parent)[0]

    raise RuntimeError(f"Not found __returning__ type by {tp!r} type")


@dataclass_transform(frozen_default=True)
class MethodMetaClass(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        class_: Any = type.__new__(cls, name, bases, namespace)

        if class_.__name__ == "Method":
            return class_

        class_ = dataclass(frozen=True)(class_)

        class_.__returning__ = get_returning_tp(class_)
        class_.__context__ = create_method_context(class_)

        return class_


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
    __context__: ClassVar[MethodContext]
    __returning__: ClassVar[type[T]]  # type: ignore[misc]
