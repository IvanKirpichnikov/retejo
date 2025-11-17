from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, TypeAlias, final

from adaptix import Mediator
from adaptix._internal.model_tools.definitions import BaseField
from adaptix._internal.morphing.model.crown_definitions import (
    BaseNameLayoutRequest,
    InpExtraMove,
    OutExtraMove,
)
from adaptix._internal.morphing.name_layout.component import (
    BuiltinStructureMaker,
    FieldAndPath,
    StructureSchema,
)
from adaptix._internal.provider.located_request import LocatedRequest
from typing_extensions import override

from retejo.entities.marker import Marker, get_marker
from retejo.error import UnmarkedFieldError

KeyPath: TypeAlias = tuple[str | int, ...]


class MarkerFieldPathMaker(BuiltinStructureMaker):
    @abstractmethod
    def make(
        self,
        marker: Marker,
        key_path: KeyPath,
    ) -> KeyPath:
        raise NotImplementedError

    @override
    def _map_fields(
        self,
        mediator: Mediator[BaseNameLayoutRequest[Any]],
        request: BaseNameLayoutRequest[Any],
        schema: StructureSchema,
        extra_move: InpExtraMove[Any] | OutExtraMove[Any],
    ) -> Iterable[FieldAndPath[Any]]:
        for field, path in super()._map_fields(
            mediator=mediator,
            request=request,
            schema=schema,
            extra_move=extra_move,
        ):
            yield self._make(field, path, request)

    @final
    def _make(
        self, field: BaseField, key_path: KeyPath | None, request: LocatedRequest[Any]
    ) -> FieldAndPath[Any]:
        if key_path is None:
            return field, key_path

        marker = get_marker(field.type)
        if marker is not None:
            return field, self.make(marker, key_path)

        raise UnmarkedFieldError(
            field_name=field.id,
            method_cls=request.loc_stack[0],
        )


class DefaultMarkerFieldPathMaker(MarkerFieldPathMaker):
    @override
    def make(
        self,
        marker: Marker,
        key_path: KeyPath,
    ) -> KeyPath:
        return marker.marker_name, *key_path
