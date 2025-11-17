from adaptix import Provider, as_is_dumper

from retejo._internal.adaptix.providers import (
    concat_provider,
    fixed_type_hint_tags_unwrapping_provider,
    omitted_provider,
)
from retejo.adaptix.method_provider import method_provider
from retejo.entities.file_obj import FileObj
from retejo.http.entities.method import HttpMethod


def method_dumper_provider() -> Provider:
    return concat_provider(
        method_provider(HttpMethod),
        as_is_dumper(FileObj),
    )


def method_result_loader_provider() -> Provider:
    return concat_provider(
        omitted_provider(),
        fixed_type_hint_tags_unwrapping_provider(),
    )
