from dataclasses import dataclass
from typing import Any, dataclass_transform, get_args, get_origin

__all__ = ["Method"]


def _get_returning(cls: Any) -> Any:
    if not issubclass(cls, Method):
        raise ValueError

    orig_bases = getattr(cls, "__orig_bases__", None)
    if orig_bases is None:
        raise ValueError

    method_base = None
    for orig_base in orig_bases:
        if get_origin(orig_base) is Method:
            method_base = orig_base

    if method_base is None:
        raise ValueError

    return get_args(method_base)[0]


@dataclass_transform(frozen_default=True)
class _MethodMetaClass(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        klass: Any = type.__new__(cls, name, bases, namespace)
        if klass.__name__ == "Method":
            return klass

        klass = dataclass(frozen=True)(klass)
        klass.__returning__ = _get_returning(klass)

        return klass


class Method[T](metaclass=_MethodMetaClass):
    @property
    def __url__(self) -> str:
        raise NotImplementedError

    @property
    def __method__(self) -> str:
        raise NotImplementedError

    # fill in meta class
    @property
    def __returning__(self) -> type[T]:
        raise NotImplementedError
