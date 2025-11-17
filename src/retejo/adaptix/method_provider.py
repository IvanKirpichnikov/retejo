from typing import Any

from adaptix import Provider, bound
from adaptix._internal.morphing.name_layout.component import BuiltinExtraMoveAndPoliciesMaker
from adaptix._internal.morphing.name_layout.provider import BuiltinNameLayoutProvider

from retejo._internal.adaptix.loc_stack_checkers import OriginSubclassLSC
from retejo._internal.adaptix.providers import OmittedSievesMarker
from retejo.adaptix.marker_field_path_maker import DefaultMarkerFieldPathMaker, MarkerFieldPathMaker
from retejo.entities.method import Method


class MethodProvider(BuiltinNameLayoutProvider):  # type: ignore[no-untyped-call]
    def __init__(
        self,
        marker_path_maker: MarkerFieldPathMaker,
    ) -> None:
        super().__init__(
            sieves_maker=OmittedSievesMarker(),
            structure_maker=marker_path_maker,
            extra_move_maker=BuiltinExtraMoveAndPoliciesMaker(),
            extra_policies_maker=BuiltinExtraMoveAndPoliciesMaker(),
        )


def method_provider(
    method_cls: type[Method[Any]] | None = None,
    marker_field_path_maker: MarkerFieldPathMaker | None = None,
) -> Provider:
    if method_cls is None:
        method_cls = Method

    if marker_field_path_maker is None:
        marker_field_path_maker = DefaultMarkerFieldPathMaker()

    return bound(
        OriginSubclassLSC(method_cls),
        MethodProvider(marker_field_path_maker),
    )
