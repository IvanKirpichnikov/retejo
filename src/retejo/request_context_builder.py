from collections.abc import Mapping
from typing import Any

from retejo.interfaces import (
    Factory,
    RequestContext,
    RequestContextBuilder,
)
from retejo.markers import BaseMarker
from retejo.method import Method


class SimpleRequestContextBuilder(RequestContextBuilder):
    _markers_factories: Mapping[type[BaseMarker], Factory]

    def __init__(self, markers_factories: Mapping[type[BaseMarker], Factory]) -> None:
        self._markers_factories = markers_factories

    def build(self, method: Method[Any]) -> RequestContext:
        context = method.__context__

        result: dict[type[BaseMarker], Any] = {}

        for marker_tp, marker_fields in context.fields.items():
            data = {}

            for marker_field in marker_fields:
                method_attr_value = getattr(method, marker_field.name)
                data[marker_field.name] = method_attr_value

            factory = self._markers_factories.get(marker_tp)
            if factory is not None:
                tp = context.types[marker_tp]
                if tp is not None:
                    data = factory.dump(data, tp)

            result[marker_tp] = data

        return result
