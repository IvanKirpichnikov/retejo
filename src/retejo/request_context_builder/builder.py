from collections.abc import Mapping
from typing import Any, override

from adaptix import Retort

from retejo.interfaces.method import Method
from retejo.interfaces.request_conext_builder import RequestContext, RequestContextBuilder
from retejo.markers.omitted import is_omitted
from retejo.request_context_builder.method_context_storage import (
    MethodContextStorage,
    RequestComponentsKey,
)


class RequestContextBuilderImpl(RequestContextBuilder):
    _method_context_storage: MethodContextStorage
    _request_components_retorts: Mapping[RequestComponentsKey, Retort]

    __slots__ = (
        "_method_context_storage",
        "_request_components_retorts",
    )

    def __init__(
        self,
        body_retort: Retort,
        url_vars_retort: Retort,
        query_params_retort: Retort,
    ) -> None:
        self._method_context_storage = MethodContextStorage()
        self._request_components_retorts = {
            RequestComponentsKey.BODY: body_retort,
            RequestComponentsKey.URL_VARS: url_vars_retort,
            RequestComponentsKey.QUERY_PARAMS: query_params_retort,
        }

    @override
    def build(self, method: Method[Any]) -> RequestContext:
        context = self._method_context_storage.get_context(type(method))

        data: dict[RequestComponentsKey, Any] = {}
        for key in RequestComponentsKey:
            prepare_data = {}

            for field in context.fields[key]:
                method_attr_value = getattr(method, field.name)
                if not is_omitted(method_attr_value):
                    prepare_data[field.name] = method_attr_value

            retort = self._request_components_retorts.get(key)
            if retort is not None:
                prepare_data = retort.dump(prepare_data, context.types[key])

            data[key] = prepare_data

        return RequestContext(
            body=data[RequestComponentsKey.BODY],
            files=data[RequestComponentsKey.FILES],
            headers=data[RequestComponentsKey.HEADERS],
            url_vars=data[RequestComponentsKey.URL_VARS],
            query_params=data[RequestComponentsKey.QUERY_PARAMS],
        )
