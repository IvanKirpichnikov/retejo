from adaptix import Omittable, P, create_loc_stack_checker  # noqa: WPS347

from retejo._internal.predicates.base import LocStackChecker, Pred
from retejo._internal.predicates.for_marker import ForMarkerLocStackChecker
from retejo.core.markers import BaseMarker, Omitted
from retejo.marker_tools.omit_tools import is_not_omitted


def for_marker(
    marker: type[BaseMarker],
    predicate: Omittable[Pred] = Omitted(),
    subclass: bool = False,
) -> LocStackChecker:
    if is_not_omitted(predicate):  # noqa: SIM108
        loc_stack_checker = create_loc_stack_checker(predicate)
    else:
        loc_stack_checker = P.ANY

    return ForMarkerLocStackChecker(
        marker=marker,
        subclass=subclass,
        loc_stack_checker=loc_stack_checker,
    )
