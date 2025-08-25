from typing import Any, cast

from adaptix import Mediator, Provider
from adaptix._internal.model_tools.definitions import NoDefault, OutputField
from adaptix._internal.morphing.model.crown_definitions import (
    LeafOutCrown,
    OutFieldCrown,
    OutputNameLayoutRequest,
    Sieve,
)
from adaptix._internal.morphing.name_layout.base import PathsTo
from adaptix._internal.morphing.name_layout.component import (
    BuiltinExtraMoveAndPoliciesMaker,
    BuiltinSievesMaker,
    BuiltinStructureMaker,
    SievesOverlay,
    apply_lsc,
)
from adaptix._internal.morphing.name_layout.provider import BuiltinNameLayoutProvider
from adaptix._internal.provider.overlay_schema import provide_schema
from typing_extensions import override

from retejo.marker_tools import is_not_omitted, is_omittable_tp


class OmittedSievesMarker(BuiltinSievesMaker):
    @override
    def make_sieves(
        self,
        mediator: Mediator[Any],
        request: OutputNameLayoutRequest,
        paths_to_leaves: PathsTo[LeafOutCrown],
    ) -> PathsTo[Sieve]:
        schema = provide_schema(SievesOverlay, mediator, request.loc_stack)
        result = {}
        for path, leaf in paths_to_leaves.items():
            if isinstance(leaf, OutFieldCrown):
                field = request.shape.fields_dict[leaf.id]
                if is_omittable_tp(field.type) or (
                    field.default != NoDefault()
                    and apply_lsc(
                        mediator,
                        request,
                        schema.omit_default,
                        field,
                    )
                ):
                    result[path] = self._create_sieve(field)
        return result

    @override
    def _create_sieve(self, field: OutputField) -> Sieve:
        if is_omittable_tp(field.type):
            return cast("Sieve", lambda obj, value=None: is_not_omitted(obj))
        else:
            return super()._create_sieve(field)


class OmittedProvider(BuiltinNameLayoutProvider):  # type: ignore[no-untyped-call]
    def __init__(self) -> None:
        super().__init__(
            sieves_maker=OmittedSievesMarker(),
            structure_maker=BuiltinStructureMaker(),
            extra_move_maker=BuiltinExtraMoveAndPoliciesMaker(),
            extra_policies_maker=BuiltinExtraMoveAndPoliciesMaker(),
        )


def omitted_provider() -> Provider:
    return OmittedProvider()
