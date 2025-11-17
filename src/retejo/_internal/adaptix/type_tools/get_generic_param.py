from typing import Any

from retejo._internal.adaptix.type_tools.parents_resolver import ParentsResolver
from retejo._internal.adaptix.type_tools.fundamentals import get_generic_args, strip_alias


def get_generic_param(
    class_: Any,
    module_name: str,
    parent_name: str,
    position_param: int,
    param_name: str,
) -> Any:
    parents = ParentsResolver().get_parents(class_)
    for parent in parents:
        origin_tp = strip_alias(parent)
        if origin_tp.__name__ == parent_name and origin_tp.__module__ == module_name:
            generic_args = get_generic_args(parent)
            return generic_args[position_param]

    raise RuntimeError(f"Not found type for {param_name!r} param by {class_!r}")
