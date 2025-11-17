from dataclasses import dataclass, field
from typing import Any, ClassVar, Generic, TypeVar

from typing_extensions import dataclass_transform

from retejo._internal.adaptix.type_tools.get_generic_param import get_generic_param


def _get_method_result(class_: Any) -> Any:
    return get_generic_param(
        class_=class_,
        module_name=__name__,
        parent_name="Method",
        position_param=0,
        param_name="__result__",
    )


@dataclass_transform(kw_only_default=True, field_specifiers=(field,))
class MethodMetaClass(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> Any:
        class_: Any = super().__new__(cls, name, bases, namespace)

        class_ = dataclass(kw_only=True)(class_)

        # It is needed to avoid setting the result for the `Method`
        if class_.__name__ != "Method" and class_.__module__ != __name__:
            class_.__result__ = _get_method_result(class_)

        return class_


_MethodResultT = TypeVar("_MethodResultT")


class Method(Generic[_MethodResultT], metaclass=MethodMetaClass):
    __result__: ClassVar[type[_MethodResultT]]  # type: ignore[misc]
