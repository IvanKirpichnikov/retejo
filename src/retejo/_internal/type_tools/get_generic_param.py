from retejo._internal.type_tools.parents_resolver import ParentsResolver
from retejo._internal.type_tools.common import TypeHint
from retejo._internal.type_tools.fundamentals import get_generic_args, strip_alias


def get_generic_param(
    tp: TypeHint,
    module_name: str,
    parent_name: str,
    position_param: int,
    param_name: str,
) -> TypeHint:
    parents = ParentsResolver().get_parents(tp)
    for parent in parents:
        origin_tp = strip_alias(parent)
        if origin_tp.__name__ == parent_name and origin_tp.__module__ == module_name:
            return get_generic_args(parent)[position_param]

    raise RuntimeError(f"Not found type for {param_name!r} param by {tp!r}")
