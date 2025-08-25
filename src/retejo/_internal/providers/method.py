from adaptix._internal.morphing.name_layout.component import (
    BuiltinExtraMoveAndPoliciesMaker,
)
from adaptix._internal.morphing.name_layout.provider import BuiltinNameLayoutProvider

from retejo._internal.providers.omitted import OmittedSievesMarker
from retejo.marker_tools.marker_field_path_maker import MarkerFieldPathMaker


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
