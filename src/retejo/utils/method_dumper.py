from collections.abc import Iterable
from typing import Any, cast

from adaptix import Mediator
from adaptix._internal.model_tools.definitions import BaseField, NoDefault, OutputField
from adaptix._internal.morphing.model.crown_definitions import (
    BaseNameLayoutRequest,
    InpExtraMove,
    LeafOutCrown,
    OutExtraMove,
    OutFieldCrown,
    OutputNameLayoutRequest,
    Sieve,
)
from adaptix._internal.morphing.name_layout.base import KeyPath, PathsTo
from adaptix._internal.morphing.name_layout.component import (
    BuiltinExtraMoveAndPoliciesMaker,
    BuiltinSievesMaker,
    BuiltinStructureMaker,
    FieldAndPath,
    SievesOverlay,
    StructureSchema,
    apply_lsc,
)
from adaptix._internal.morphing.name_layout.provider import BuiltinNameLayoutProvider
from adaptix._internal.provider.overlay_schema import provide_schema

from retejo.markers.base import get_marker
from retejo.markers.omitted import is_omittable_tp, is_omitted


class _MethodSievesMaker(BuiltinSievesMaker):
    def _create_sieve(self, field: OutputField) -> Sieve:
        if is_omittable_tp(field.type):
            return cast("Sieve", lambda obj, value=None: not is_omitted(obj))
        else:
            return super()._create_sieve(field)

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


class _MethodDumperStructureMaker(BuiltinStructureMaker):
    def _map_fields(
        self,
        mediator: Mediator,
        request: BaseNameLayoutRequest,
        schema: StructureSchema,
        extra_move: InpExtraMove | OutExtraMove,
    ) -> Iterable[FieldAndPath]:
        for field, path in super()._map_fields(
            mediator=mediator,
            request=request,
            schema=schema,
            extra_move=extra_move,
        ):
            yield self._custom_map(field, path)

    def _custom_map(self, field: BaseField, path: KeyPath | None) -> FieldAndPath:
        if path is None:
            return field, path

        marker = get_marker(field.type)
        if not marker:
            raise ValueError

        return field, (marker.name, *path)


class MethodDumperProvider(BuiltinNameLayoutProvider):
    def __init__(self) -> None:
        super().__init__(
            sieves_maker=_MethodSievesMaker(),
            structure_maker=_MethodDumperStructureMaker(),
            extra_move_maker=BuiltinExtraMoveAndPoliciesMaker(),
            extra_policies_maker=BuiltinExtraMoveAndPoliciesMaker(),
        )
