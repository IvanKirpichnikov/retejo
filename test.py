from abc import ABC
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Annotated, Any, ClassVar, TypeAlias, TypeGuard, TypeVar, cast

from adaptix import Loader, Mediator, P, Provider, Retort, bound, dumper
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

from adaptix._internal.morphing.generic_provider import TypeHintTagsUnwrappingProvider
from adaptix._internal.morphing.request_cls import LoaderRequest
from adaptix._internal.morphing.name_layout.provider import BuiltinNameLayoutProvider
from adaptix._internal.provider.essential import DirectMediator
from adaptix._internal.provider.loc_stack_filtering import (
    LocStack,
    LocStackChecker,
    OriginSubclassLSC,
    Pred,
    create_loc_stack_checker,
)
from adaptix._internal.provider.loc_stack_tools import find_owner_with_field
from adaptix._internal.provider.location import FieldLoc, OutputFieldLoc, TypeHintLoc
from adaptix._internal.provider.overlay_schema import provide_schema
from adaptix._internal.type_tools.norm_utils import _TYPE_TAGS
from adaptix._internal.type_tools.normalize_type import BaseNormType, normalize_type


def is_normalize_type(tp: Any) -> TypeGuard[BaseNormType]:
    return isinstance(tp, BaseNormType)


def strip_tag(norm: BaseNormType) -> BaseNormType:
    if norm.origin in _TYPE_TAGS:
        return norm.args[0]
    return norm


class Omitted:
    def __bool__(self) -> bool | None:
        return False

    def __repr__(self) -> str:
        return "<Omitted>"


def is_omitted(value: Any) -> TypeGuard[Omitted]:
    return isinstance(value, Omitted)


def is_omittable_tp(tp: Any) -> bool:
    norm_tp = normalize_type(tp) if not isinstance(tp, BaseNormType) else tp
    for arg in norm_tp.args:
        if is_normalize_type(arg):
            arg = arg.source

        if arg is Omitted:
            return True

    strip_norm_tp = strip_tag(norm_tp)
    if strip_norm_tp is norm_tp:
        return False

    return is_omittable_tp(strip_norm_tp)

class FixedTypeHintTagsUnwrappingProvider(TypeHintTagsUnwrappingProvider):
    def _provide_proxy(self, mediator: Mediator, request: LoaderRequest) -> Loader:
        return mediator.mandatory_provide(
            request.with_loc_stack(
                request.loc_stack.append_with(
                    TypeHintLoc(self._get_proxy_target(request.loc_stack.last.type))
                ),
            ),
            lambda x: self._get_error_text(),
        )


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


def method_dumper() -> Provider:
    return bound(
        OriginSubclassLSC(Method),
        MethodDumperProvider(),
    )


class BaseMarker(ABC):
    name: ClassVar[str]

    def __repr__(self) -> str:
        return f'<Marker "{self.name}">'


def get_marker(tp: Any) -> BaseMarker | None:
    norm_tp = normalize_type(tp) if not isinstance(tp, BaseNormType) else tp

    for arg in norm_tp.args:
        if is_normalize_type(arg):
            arg = arg.source

        if isinstance(arg, BaseMarker):
            return arg

    strip_norm_tp = strip_tag(norm_tp)
    if strip_norm_tp is norm_tp:
        return None

    return get_marker(strip_norm_tp)


class ForMarkerPredicate(LocStackChecker):
    def __init__(
        self,
        predicate: Pred,
        marker_tp: type[BaseMarker],
        is_subclass: bool = False,
    ) -> None:
        self.loc_stack_checker = create_loc_stack_checker(predicate)
        self.marker_tp = marker_tp
        self.is_subclass = is_subclass

    def check_loc_stack(self, mediator: DirectMediator, loc_stack: LocStack[OutputFieldLoc]) -> bool:
        # print(loc_stack)j

        try:
            _owner_loc, field_loc = find_owner_with_field(loc_stack)
        except ValueError:
            return False
        print(loc_stack.last.type, loc_stack, sep="\n", end="\n\n")
        return self._check_field_loc(field_loc) and self.loc_stack_checker.check_loc_stack(mediator, loc_stack)

    def _check_field_loc(self, loc: FieldLoc) -> bool:
        try:
            marker = get_marker(loc.type)
        except ValueError:
            return False

        if marker is None:
            return False

        if self.is_subclass:
            return issubclass(type(marker), self.marker_tp)
        else:
            return type(marker) is self.marker_tp


class QueryParamMarker(BaseMarker):
    name = "QueryParam"


T = TypeVar("T")
QueryParam: TypeAlias = Annotated[T, QueryParamMarker()]


@dataclass
class Method:
    a: QueryParam[str | None]


retort = Retort(
    recipe=[
        FixedTypeHintTagsUnwrappingProvider(),
        method_dumper(),
        dumper(
            ForMarkerPredicate(
                P[str | None],
                QueryParamMarker,
            ),
            lambda x: "null",
        ),
    ]
)


print(retort.dump(Method(None)))
