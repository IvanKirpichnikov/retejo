from typing import Any

from adaptix._internal.provider.essential import DirectMediator
from adaptix._internal.provider.loc_stack_filtering import (
    LocStack,
    LocStackChecker,
)
from adaptix._internal.provider.location import TypeHintLoc


class WithParentsPredicate(LocStackChecker):
    def __init__(self, *tps: Any) -> None:
        self._tps = tps

    def check_loc_stack(self, mediator: DirectMediator, loc_stack: LocStack[TypeHintLoc]) -> bool:
        return issubclass(loc_stack.last.type, self._tps)
