from collections.abc import MutableMapping
from typing import Any

from pydantic import TypeAdapter

from retejo.integrations.common.base import BaseClient, MarkersFactorties
from retejo.interfaces import Factory
from retejo.markers.body import BodyMarker
from retejo.markers.header import HeaderMarker
from retejo.markers.query_param import QueryParamMarker
from retejo.markers.url_var import UrlVarMarker


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

    def load(self, data: Any, tp: Any, /) -> Any:
        type_adapter = self._get_type_adapter(tp)
        return type_adapter.validate_python(data)

    def dump(self, data: Any, tp: Any | None = None, /) -> Any:
        type_adapter = self._get_type_adapter(tp)
        return type_adapter.dump_python(data, exclude_unset=True)


class BasePydanticClient(BaseClient[PydanticFactory]):
    def init_markers_factories(self) -> MarkersFactorties[PydanticFactory]:
        factory = PydanticFactory()

        return {
            BodyMarker: factory,
            UrlVarMarker: factory,
            HeaderMarker: factory,
            QueryParamMarker: factory,
        }

    def init_response_factory(self) -> PydanticFactory:
        return PydanticFactory()
