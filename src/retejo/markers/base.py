from typing import (
    Annotated,
    Any,
    Protocol,
    TypeVar,
    Union,
    get_args,
    get_origin,
    runtime_checkable,
)


@runtime_checkable
class _OriginTp(Protocol):
    origin_tp: Any


class BaseMarker:
    origin_tp: Any

    def __init__(self, origin_tp: Any) -> None:
        self.origin_tp = origin_tp


T_co = TypeVar("T_co", bound=BaseMarker, covariant=True)


def get_markers(obj: Any) -> list[BaseMarker] | None:
    if get_origin(obj) is Annotated:
        args = obj.__metadata__
        res = [arg for arg in args if isinstance(arg, BaseMarker)]
        if not res:
            return None
        return res
    return None


def _get_origin_tps(obj: Any) -> list[_OriginTp] | None:
    if get_origin(obj) is Annotated:
        args = obj.__metadata__
        res = [arg for arg in args if isinstance(arg, _OriginTp)]
        if not res:
            return None
        return res
    return None


def get_value_marker(obj: Any) -> Any:
    if get_origin(obj) is Annotated:
        origin_tps = _get_origin_tps(obj)
        if origin_tps:
            return Union[tuple(origin_tp.origin_tp for origin_tp in origin_tps)]  # noqa: UP007

    args = get_args(obj)

    if len(args) == 1:
        return get_value_marker(args[0])

    return obj
