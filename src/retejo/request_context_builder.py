from collections.abc import Mapping
from typing import Any, override

from retejo.interfaces import (
    Factory,
    RequestContext,
    RequestContextBuilder,
)
from retejo.markers import BaseMarker, is_omitted
from retejo.method import Method


class SimpleRequestContextBuilder(RequestContextBuilder):
    _markers_factories: Mapping[type[BaseMarker], Factory]

    def __init__(self, markers_factories: Mapping[type[BaseMarker], Factory]) -> None:
        self._markers_factories = markers_factories

    @override
    def build(self, method: Method[Any]) -> RequestContext:
        context = method.__context__

        result: dict[type[BaseMarker], Any] = {}

        for marker_tp, marker_fields in context.fields.items():
            data = {}

            for marker_filed in marker_fields:
                method_attr_value = getattr(method, marker_filed.name)
                if not is_omitted(method_attr_value):
                    data[marker_filed.name] = method_attr_value

            factory = self._markers_factories.get(marker_tp)
            if factory is not None:
                tp = context.types[marker_tp]
                if tp is not None:
                    data = factory.dump(data, tp)

            result[marker_tp] = data

        return result
