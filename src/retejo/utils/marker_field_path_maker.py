from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, final

from adaptix import Mediator
from adaptix._internal.model_tools.definitions import BaseField
from adaptix._internal.morphing.model.crown_definitions import BaseNameLayoutRequest, InpExtraMove, OutExtraMove
from adaptix._internal.morphing.name_layout.base import KeyPath
from adaptix._internal.morphing.name_layout.component import (
    BuiltinStructureMaker,
    FieldAndPath,
    StructureSchema,
)

from retejo.core.markers import BaseMarker, get_marker

__all__ = ("BaseMarkerFieldPathMaker", "KeyPath", "MarkerFieldPathMaker")


class BaseMarkerFieldPathMaker(BuiltinStructureMaker, ABC):
    @abstractmethod
    def make(
        self,
        marker: BaseMarker,
        key_path: KeyPath,
    ) -> KeyPath:
        raise NotImplementedError

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
            yield self._make(field, path)

    @final
    def _make(self, field: BaseField, key_path: KeyPath | None) -> FieldAndPath[Any]:
        if key_path is None:
            return field, key_path

        marker = get_marker(field.type)
        if not marker:
            raise ValueError

        return field, self.make(marker, key_path)


class MarkerFieldPathMaker(BaseMarkerFieldPathMaker):
    def make(
        self,
        marker: BaseMarker,
        key_path: KeyPath,
    ) -> KeyPath:
        return marker.name, *key_path
