from typing import Any, cast

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
from adaptix._internal.morphing.name_layout.provider import (
    BuiltinNameLayoutProvider,
)
from adaptix._internal.provider.essential import Mediator
from adaptix._internal.provider.overlay_schema import provide_schema

from retejo.markers import is_omittable
from retejo.markers.omitted import is_omitted


class OmitSievesMaker(BuiltinSievesMaker):
    def _create_sieve(self, field: OutputField) -> Sieve:
        if is_omittable(field.type):  # type: ignore[redundant-expr]
            return cast("Sieve", lambda obj, value=None: not is_omitted(obj))
        else:
            return super()._create_sieve(field)  # type: ignore[unreachable]

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
                if is_omittable(field.type) or (  # type: ignore[redundant-expr]
                    field.default != NoDefault()  # type: ignore[unreachable]
                    and apply_lsc(
                        mediator,
                        request,
                        schema.omit_default,
                        field,
                    )
                ):
                    result[path] = self._create_sieve(field)
        return result


class OmitOmittedFieldProvider(BuiltinNameLayoutProvider):
    def __init__(self) -> None:
        super().__init__(
            structure_maker=BuiltinStructureMaker(),
            sieves_maker=OmitSievesMaker(),
            extra_move_maker=BuiltinExtraMoveAndPoliciesMaker(),
            extra_policies_maker=BuiltinExtraMoveAndPoliciesMaker(),
        )
