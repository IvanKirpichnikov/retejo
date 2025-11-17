from typing import Annotated, Any, get_args, get_origin

from adaptix import P, create_loc_stack_checker  # noqa: WPS347
from typing_extensions import override

from retejo._internal.adaptix.loc_stack_checkers import (
    ForMarkerLocStackChecker,
    LocStackChecker,
    Pred,
)
from retejo.entities.marker import Marker
from retejo.omit import Omittable, Omitted, is_not_omitted, is_omitted


def _get_origin_marker(marker: Any) -> Marker | None:
    if isinstance(marker, Marker):
        return marker
    elif get_origin(marker) is Annotated:
        annotated_args = get_args(marker)
        marker_args = tuple(
            annotated_arg for annotated_arg in annotated_args if isinstance(annotated_arg, Marker)
        )

        if len(marker_args) == 1:
            return marker_args[0]
        else:
            return None
    else:
        return None


class IncorrectMarkerValueError(ValueError):
    def __init__(
        self,
        incorrect_marker: Any,
    ) -> None:
        super().__init__(incorrect_marker)
        self._incorrect_marker = incorrect_marker

    @property
    def incorrect_marker(self) -> Any:
        return self._incorrect_marker

    @override
    def __str__(self) -> str:
        return f"Can't get a marker from the {self._incorrect_marker!r} object"

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._incorrect_marker!r})"


def for_marker(
    marker: Any,
    predicate: Omittable[Pred] = Omitted(),
    subclass: Omittable[bool] = Omitted(),
) -> LocStackChecker:
    origin_marker = _get_origin_marker(marker)
    if origin_marker is None:
        raise IncorrectMarkerValueError(marker)

    if is_not_omitted(predicate):  # noqa: SIM108
        loc_stack_checker = create_loc_stack_checker(predicate)
    else:
        loc_stack_checker = P.ANY

    if is_omitted(subclass):
        subclass = False

    return ForMarkerLocStackChecker(
        marker=origin_marker,
        subclass=subclass,
        loc_stack_checker=loc_stack_checker,
    )
