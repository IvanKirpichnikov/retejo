from collections.abc import MutableMapping
from typing import Any, override

from pydantic import TypeAdapter

from retejo.integrations.common.base import BaseClient, MarkersFactorties
from retejo.interfaces import Factory
from retejo.markers import (
    BodyMarker,
    HeaderMarker,
    QueryParamMarker,
    UrlVarMarker,
)


class PydanticFactory(Factory):
    _cache_type_adapters: MutableMapping[Any, TypeAdapter]

    def __init__(self) -> None:
        self._cache_type_adapters = {}

    def _get_type_adapter(self, tp: Any) -> TypeAdapter:
        type_adapter_cache = self._cache_type_adapters.get(tp)
        if type_adapter_cache is not None:
            return type_adapter_cache

        type_adapter = TypeAdapter(tp)
        self._cache_type_adapters[tp] = type_adapter
        return type_adapter

    @override
    def load(self, data: Any, tp: Any, /) -> Any:
        type_adapter = self._get_type_adapter(tp)
        return type_adapter.validate_python(data)

    @override
    def dump(self, data: Any, tp: Any | None = None, /) -> Any:
        type_adapter = self._get_type_adapter(tp)
        return type_adapter.dump_python(data, exclude_unset=True)


class BasePydanticClient(BaseClient):
    @override
    def init_markers_factories(self) -> MarkersFactorties:
        factory = PydanticFactory()

        return {
            BodyMarker: factory,
            UrlVarMarker: factory,
            HeaderMarker: factory,
            QueryParamMarker: factory,
        }

    @override
    def init_response_factory(self) -> Factory:
        return PydanticFactory()
