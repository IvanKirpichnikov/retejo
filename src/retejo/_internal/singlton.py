from collections.abc import MutableMapping
from typing import Any, ClassVar, override


class SingletonMeta(type):
    _instances: ClassVar[MutableMapping[Any, Any]] = {}

    @override
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
