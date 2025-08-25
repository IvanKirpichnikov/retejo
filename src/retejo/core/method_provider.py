from typing import TYPE_CHECKING, Any

from adaptix import Provider, as_sentinel, bound

from retejo._internal.predicates.origin_subclass import OriginSubclassLSC
from retejo._internal.providers.concat import concat_provider
from retejo._internal.providers.fixed_tp_tags_unwrapping import (
    fixed_type_hint_tags_unwrapping_provider,
)
from retejo._internal.providers.method import MethodProvider
from retejo._internal.providers.omitted import omitted_provider
from retejo.core.markers import Omittable, Omitted
from retejo.marker_tools.marker_field_path_maker import (
    DefaultMarkerFieldPathMaker,
    MarkerFieldPathMaker,
)
from retejo.marker_tools.omit_tools import is_omitted

if TYPE_CHECKING:
    from retejo.core.entities import Method


def method_provider(
    method_tp: Omittable[type["Method[Any]"]] = Omitted(),
    marker_path_maker: Omittable[MarkerFieldPathMaker] = Omitted(),
) -> Provider:
    if is_omitted(method_tp):
        from retejo.core.entities import Method

        method_tp = Method

    if is_omitted(marker_path_maker):
        marker_path_maker = DefaultMarkerFieldPathMaker()

    return concat_provider(
        fixed_type_hint_tags_unwrapping_provider(),
        as_sentinel(Omitted),
        bound(
            OriginSubclassLSC(method_tp),
            MethodProvider(marker_path_maker),
        ),
        omitted_provider(),
    )
