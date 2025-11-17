from collections.abc import Callable

from adaptix._internal.provider.essential import DirectMediator
from adaptix._internal.provider.loc_stack_filtering import (
    LocStack,
    LocStackChecker,
    OriginSubclassLSC,
    Pred,
)
from adaptix._internal.provider.loc_stack_tools import find_owner_with_field
from adaptix._internal.provider.location import FieldLoc, OutputFieldLoc
from typing_extensions import override

from retejo._internal.adaptix.type_tools.basic_utils import is_subclass_soft
from retejo.entities.marker import Marker, get_marker

__all__ = ("ForMarkerLocStackChecker", "LocStackChecker", "OriginSubclassLSC", "Pred")


class ForMarkerLocStackChecker(LocStackChecker):
    __slots__ = (
        "_checker",
        "_loc_stack_checker",
        "_marker",
        "_subclass",
    )

    _checker: Callable[[type[Marker]], bool]

    def __init__(
        self,
        loc_stack_checker: LocStackChecker,
        marker: Marker,
        subclass: bool = False,
    ) -> None:
        marker_tp = type(marker)

        self._marker = marker
        self._subclass = subclass
        self._loc_stack_checker = loc_stack_checker

        if subclass:
            self._checker = lambda marker: is_subclass_soft(marker, marker_tp)
        else:
            self._checker = lambda marker: marker is marker_tp

    @override
    def __repr__(self) -> str:
        kwargs = (
            f"loc_stack_checker={self._loc_stack_checker}, "
            f"marker={self._marker}, "
            f"subclass={self._subclass}"
        )
        return f"<{self.__class__.__name__}({kwargs})>"

    @override
    def check_loc_stack(
        self, mediator: DirectMediator, loc_stack: LocStack[OutputFieldLoc]
    ) -> bool:
        try:
            _, field_loc = find_owner_with_field(loc_stack)
        except ValueError:
            return False

        return self._check_field_loc(field_loc) and self._loc_stack_checker.check_loc_stack(
            mediator, loc_stack
        )

    def _check_field_loc(self, loc: FieldLoc) -> bool:
        try:
            marker = get_marker(loc.type)
        except ValueError:
            return False

        if marker is None:
            return False

        return self._checker(type(marker))
