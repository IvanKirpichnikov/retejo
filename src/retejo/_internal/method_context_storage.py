from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from dataclasses import Field, dataclass, fields as get_fields
from enum import Enum
from typing import Any, NotRequired, TypedDict

from retejo.interfaces.method import Method
from retejo.markers import (
    is_body,
    is_file,
    is_header,
    is_marker,
    is_omittable,
    is_query_param,
    is_url_var,
)


class RequestComponentsKey(Enum):
    BODY = "body"
    HEADERS = "headers"
    URL_VARS = "url_vars"
    QUERY_PARAMS = "query_params"
    FILES = "files"


@dataclass
class MethodContext:
    fields: Mapping[RequestComponentsKey, Iterable[Field[Any]]]
    types: Mapping[RequestComponentsKey, type[Any] | None]


class MethodContextStorage:
    _cache: MutableMapping[type[Method[Any]], MethodContext]

    __slots__ = ("_cache",)

    def __init__(self) -> None:
        self._cache = {}

    def get_context(self, method_tp: type[Method[Any]]) -> MethodContext:
        cache_context = self._cache.get(method_tp)
        if cache_context is not None:
            return cache_context

        context = self._make_context(method_tp)

        self._cache[method_tp] = context

        return context

    def _make_context(
        self,
        method_tp: type[Method[Any]],
    ) -> MethodContext:
        fields = self._sort_fields(get_fields(method_tp))
        types = {}

        for key in RequestComponentsKey:
            types[key] = self._make_type(
                method_tp=method_tp,
                component_name=key,
                fields=fields[key],
            )

        return MethodContext(
            types=types,
            fields=fields,
        )

    def _sort_fields(
        self,
        fields: Sequence[Field[Any]],
    ) -> Mapping[RequestComponentsKey, Sequence[Field[Any]]]:
        result: dict[RequestComponentsKey, list[Field[Any]]] = defaultdict(list)

        for field in fields:
            if not is_marker(field.type):
                continue

            if is_body(field.type):
                result[RequestComponentsKey.BODY].append(field)
            if is_header(field.type):
                result[RequestComponentsKey.HEADERS].append(field)
            if is_url_var(field.type):
                result[RequestComponentsKey.URL_VARS].append(field)
            if is_query_param(field.type):
                result[RequestComponentsKey.QUERY_PARAMS].append(field)
            if is_file(field.type):
                result[RequestComponentsKey.FILES].append(field)

        return result

    def _make_type(
        self,
        method_tp: type[Method[Any]],
        component_name: RequestComponentsKey,
        fields: Sequence[Field[Any]],
    ) -> Any | None:
        if not fields:
            return None

        name = f"{method_tp.__name__}{component_name.name}Type"

        fields_tp: MutableMapping[str, Any] = {}
        for field in fields:
            if is_omittable(field.type):
                fields_tp[field.name] = NotRequired[field.type]
            else:
                fields_tp[field.name] = field.type

        return TypedDict(name, fields_tp)  # type: ignore[operator]
