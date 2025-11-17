from typing import Any, cast

from adaptix import Chain, Loader, Mediator, Provider, as_sentinel
from adaptix._internal.model_tools.definitions import NoDefault, OutputField
from adaptix._internal.morphing.generic_provider import TypeHintTagsUnwrappingProvider
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
from adaptix._internal.morphing.request_cls import LoaderRequest
from adaptix._internal.provider.location import TypeHintLoc
from adaptix._internal.provider.overlay_schema import provide_schema
from adaptix._internal.provider.provider_wrapper import ChainingProvider, ConcatProvider
from typing_extensions import override

from retejo.omit import Omitted, is_not_omitted, is_omittable_tp


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
            # value=None is worth it because a bug was found in adaptix
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


class _FixedTypeHintTagsUnwrappingProvider(TypeHintTagsUnwrappingProvider):
    @override
    def _provide_proxy(self, mediator: Mediator[Any], request: LoaderRequest) -> Loader[Any]:
        return mediator.mandatory_provide(
            request.with_loc_stack(
                request.loc_stack.append_with(
                    TypeHintLoc(self._get_proxy_target(request.loc_stack.last.type))
                ),
            ),
            lambda provide: self._get_error_text(),
        )


def omitted_provider() -> Provider:
    return concat_provider(
        as_sentinel(Omitted),
        OmittedProvider(),
    )


def fixed_type_hint_tags_unwrapping_provider() -> Provider:
    return _FixedTypeHintTagsUnwrappingProvider()


def concat_provider(*providers: Provider) -> Provider:
    return ConcatProvider(*providers)


def chaining_provider(chain: Chain, provider: Provider) -> Provider:
    return ChainingProvider(
        chain=chain,
        provider=provider,
    )
