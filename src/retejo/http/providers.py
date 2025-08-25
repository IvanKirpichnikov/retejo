from adaptix import Provider, as_is_dumper, as_sentinel

from retejo._internal.providers.concat import concat_provider
from retejo._internal.providers.fixed_tp_tags_unwrapping import (
    fixed_type_hint_tags_unwrapping_provider,
)
from retejo.core.markers import Omitted
from retejo.core.method_provider import method_provider
from retejo.http.entities import FileObj, HttpMethod
from retejo.http.mapping_utils import mapping_response_data


def http_method_dumper_provider() -> Provider:
    return concat_provider(
        method_provider(HttpMethod),
        as_is_dumper(FileObj),
        fixed_type_hint_tags_unwrapping_provider(),
    )


def http_response_loader_provider() -> Provider:
    return concat_provider(
        as_sentinel(Omitted),
        fixed_type_hint_tags_unwrapping_provider(),
        mapping_response_data(),
    )
