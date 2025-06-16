from collections.abc import Mapping
from typing import Any, override

from retejo._internal.method_context_storage import (
    MethodContextStorage,
    RequestComponentsKey,
)
from retejo.interfaces.factory import Factory
from retejo.interfaces.method import Method
from retejo.interfaces.request_context_builder import RequestContext, RequestContextBuilder
from retejo.markers import is_omitted


class RequestContextBuilderImpl(RequestContextBuilder):
    _method_context_storage: MethodContextStorage
    _request_components_factories: Mapping[RequestComponentsKey, Factory]

    __slots__ = (
        "_method_context_storage",
        "_request_components_factories",
    )

    def __init__(
        self,
        body_factory: Factory,
        url_vars_factory: Factory,
        query_params_factory: Factory,
    ) -> None:
        self._method_context_storage = MethodContextStorage()
        self._request_components_factories = {
            RequestComponentsKey.BODY: body_factory,
            RequestComponentsKey.URL_VARS: url_vars_factory,
            RequestComponentsKey.QUERY_PARAMS: query_params_factory,
        }

    @override
    def build(self, method: Method[Any]) -> RequestContext:
        context = self._method_context_storage.get_context(type(method))

        result: dict[str, Any] = {}
        for key in RequestComponentsKey:
            data = {}

            for field in context.fields[key]:
                method_attr_value = getattr(method, field.name)
                if not is_omitted(method_attr_value):
                    data[field.name] = method_attr_value

            factory = self._request_components_factories.get(key)
            if factory is not None:
                tp = context.types[key]
                if tp is not None:
                    data = factory.dump(data, context.types[key])

            result[key.value] = data

        return RequestContext(**result)
