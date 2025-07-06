from dataclasses import dataclass
from typing import Any, ClassVar, Generic, TypeVar

from typing_extensions import dataclass_transform

from retejo._adaptix.type_tools.fundamentals import get_generic_args, strip_alias
from retejo.utils.parents_resolver import ParentsResolver


def get_returning_tp(tp: Any) -> Any:
    parents = ParentsResolver().get_parents(tp)

    for parent in parents:
        if strip_alias(parent) is Method:
            return get_generic_args(parent)[0]

    raise RuntimeError(f"Not found __returning__ type by {tp!r} type")


@dataclass_transform(frozen_default=True, kw_only_default=True)
class MethodMetaClass(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        class_: Any = super().__new__(cls, name, bases, namespace)

        if "__slots__" not in namespace:
            class_ = dataclass(
                frozen=True,
                slots=True,
                kw_only=True,
            )(class_)

        if class_.__name__ != "Method":
            class_.__returning__ = get_returning_tp(class_)

        return class_


T = TypeVar("T")


class Method(Generic[T], metaclass=MethodMetaClass):
    __slots__ = (
        "__method__",
        "__returning__",
        "__url__",
    )

    __url__: ClassVar[str]
    __method__: ClassVar[str]

    # fill in meta class
    __returning__: ClassVar[type[T]]  # type: ignore[misc]
