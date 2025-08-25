from adaptix._internal.provider.essential import DirectMediator
from adaptix._internal.provider.loc_stack_filtering import LocStack, LocStackChecker
from adaptix._internal.provider.location import TypeHintLoc
from typing_extensions import override

from retejo._internal.type_tools.basic_utils import is_subclass_soft
from retejo._internal.type_tools.common import TypeHint
from retejo._internal.type_tools.normalize_type import normalize_type


class FisrtStackElementChecker(LocStackChecker):
    def __init__(self, tp: TypeHint) -> None:
        self._tp = normalize_type(tp).origin

    @override
    def check_loc_stack(self, mediator: DirectMediator, loc_stack: LocStack[TypeHintLoc]) -> bool:
        try:
            first = normalize_type(loc_stack[0].type)
        except ValueError:
            return False

        return is_subclass_soft(first.origin, self._tp)
