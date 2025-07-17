from typing import Any, cast

from adaptix import Mediator, Provider, as_sentinel, bound
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
    SievesOverlay,
    apply_lsc,
)
from adaptix._internal.morphing.name_layout.provider import BuiltinNameLayoutProvider
from adaptix._internal.provider.loc_stack_filtering import OriginSubclassLSC
from adaptix._internal.provider.overlay_schema import provide_schema
from adaptix._internal.provider.provider_wrapper import ConcatProvider

from retejo.core.entities import Method
from retejo.core.markers import Omitted, is_omittable_tp, is_omitted
from retejo.utils._fixed_type_hint_tags_unwrapping_provider import FixedTypeHintTagsUnwrappingProvider
from retejo.utils.marker_field_path_maker import BaseMarkerFieldPathMaker, MarkerFieldPathMaker


class _MethodSievesMaker(BuiltinSievesMaker):
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

    def _create_sieve(self, field: OutputField) -> Sieve:
        if is_omittable_tp(field.type):
            return cast("Sieve", lambda obj, value=None: not is_omitted(obj))
        else:
            return super()._create_sieve(field)


class MethodDumperProvider(BuiltinNameLayoutProvider):  # type: ignore[no-untyped-call]
    def __init__(
        self,
        marker_path_maker: BaseMarkerFieldPathMaker,
    ) -> None:
        super().__init__(
            sieves_maker=_MethodSievesMaker(),
            structure_maker=marker_path_maker,
            extra_move_maker=BuiltinExtraMoveAndPoliciesMaker(),
            extra_policies_maker=BuiltinExtraMoveAndPoliciesMaker(),
        )


def method_provider(
    method_tp: type[Method[Any]] | None = None,
    marker_path_maker: BaseMarkerFieldPathMaker | None = None,
) -> Provider:
    if method_tp is None:
        method_tp = Method

    if marker_path_maker is None:
        marker_path_maker = MarkerFieldPathMaker()

    return ConcatProvider(
        as_sentinel(Omitted),
        FixedTypeHintTagsUnwrappingProvider(),
        bound(
            OriginSubclassLSC(method_tp),
            MethodDumperProvider(marker_path_maker),
        ),
    )
