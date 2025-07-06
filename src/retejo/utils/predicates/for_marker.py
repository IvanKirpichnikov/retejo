from typing import TYPE_CHECKING, cast

from adaptix._internal.provider.essential import DirectMediator
from adaptix._internal.provider.loc_stack_filtering import (
    LocStack,
    LocStackChecker,
)
from adaptix._internal.provider.location import OutputFieldLoc, TypeHintLoc

from retejo._adaptix.type_tools.fundamentals import get_all_type_hints
from retejo.markers.base import BaseMarker, get_marker

if TYPE_CHECKING:
    from adaptix.struct_trail import Attr


# TODO: edit
class ForMarkerPredicate(LocStackChecker):
    def __init__(
        self,
        marker_tp: type[BaseMarker],
        is_subclass: bool = False,
    ) -> None:
        self.marker_tp = marker_tp
        self.is_subclass = is_subclass

    def check_loc_stack(self, mediator: DirectMediator, loc_stack: LocStack[TypeHintLoc]) -> bool:
        orig_cls = loc_stack[0].type
        field_name = cast("Attr", cast("OutputFieldLoc", loc_stack[1]).accessor.trail_element).name

        marker = get_marker(get_all_type_hints(orig_cls)[field_name])

        if marker is None:
            return False

        if self.is_subclass:
            return issubclass(type(marker), self.marker_tp)
        return type(marker) is self.marker_tp
