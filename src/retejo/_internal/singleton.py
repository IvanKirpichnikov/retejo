from typing import Any

from typing_extensions import override


def _singleton_repr(self: Any) -> str:
    return f"{type(self).__name__}()"


def _singleton_hash(self: Any) -> int:
    return hash(type(self))


def _singleton_copy(self: Any) -> Any:
    return self


def _singleton_deepcopy(self: Any, memo: Any) -> Any:
    return self


def _singleton_new(cls: Any) -> Any:
    return cls._instance


class SingletonMeta(type):
    _instance: Any

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        namespace.setdefault("__repr__", _singleton_repr)
        namespace.setdefault("__str__", _singleton_repr)
        namespace.setdefault("__hash__", _singleton_hash)
        namespace.setdefault("__copy__", _singleton_copy)
        namespace.setdefault("__deepcopy__", _singleton_deepcopy)
        namespace.setdefault("__slots__", ())

        class_ = super().__new__(cls, name, bases, namespace, **kwargs)

        instance = super().__call__(class_)
        class_._instance = instance
        if "__new__" not in class_.__dict__:
            class_.__new__ = _singleton_new  # type: ignore[method-assign, assignment]
        return class_

    @override
    def __call__(cls) -> Any:
        return cls._instance
