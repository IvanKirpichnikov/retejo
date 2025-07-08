from adaptix._internal.provider.essential import DirectMediator
from adaptix._internal.provider.loc_stack_filtering import LocStack, LocStackChecker, Pred, create_loc_stack_checker
from adaptix._internal.provider.loc_stack_tools import find_owner_with_field
from adaptix._internal.provider.location import FieldLoc, OutputFieldLoc

from retejo.core.markers import BaseMarker, get_marker


class ForMarkerLocStackChecker(LocStackChecker):
    def __init__(
        self,
        loc_stack_checker: LocStackChecker,
        marker: type[BaseMarker],
        subclass: bool = False,
    ) -> None:
        self.loc_stack_checker = loc_stack_checker
        self.marker = marker
        self.subclass = subclass

    def check_loc_stack(self, mediator: DirectMediator, loc_stack: LocStack[OutputFieldLoc]) -> bool:
        # print(loc_stack)j

        try:
            owner_loc, field_loc = find_owner_with_field(loc_stack)
        except ValueError:
            return False

        return self._check_field_loc(field_loc) and self.loc_stack_checker.check_loc_stack(mediator, loc_stack)

    def _check_field_loc(self, loc: FieldLoc) -> bool:
        try:
            marker = get_marker(loc.type)
        except ValueError:
            return False

        if marker is None:
            return False

        if self.subclass:
            return issubclass(type(marker), self.marker)
        else:
            return type(marker) is self.marker


def for_marker(
    predicate: Pred,
    marker: type[BaseMarker],
    subclass: bool = False,
) -> LocStackChecker:
    return ForMarkerLocStackChecker(
        marker=marker,
        subclass=True,
        loc_stack_checker=create_loc_stack_checker(predicate),
    )
