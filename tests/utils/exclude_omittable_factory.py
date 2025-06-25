from typing import Any

from retejo.interfaces.factory import Factory
from retejo.markers.omitted import is_omitted


class ExludeOmittableFactory(Factory):
    def load(self, data: Any, tp: Any, /) -> Any:
        return data

    def dump(self, data: Any, tp: Any | None = None, /) -> Any:
        result = {}
        for key, value in data.items():
            if not is_omitted(value):
                result[key] = value  # noqa: PERF403
        return result
