from collections import defaultdict
from collections.abc import Mapping, MutableMapping, Sequence
from dataclasses import Field, dataclass, fields as get_fields
from typing import TYPE_CHECKING, Any, TypedDict

from retejo.markers.base import BaseMarker, get_marker_type

if TYPE_CHECKING:
    from retejo.method.method import Method


@dataclass(slots=True, frozen=True)
class MethodContext:
    fields: Mapping[type[BaseMarker], Sequence[Field[Any]]]
    types: Mapping[type[BaseMarker], type[Any] | None]


def create_method_context(method_tp: "type[Method[Any]]") -> MethodContext:
    fields = get_marker_fields(get_fields(method_tp))

    types = {}
    for marker_tp, marker_fields in fields.items():
        types[marker_tp] = make_typed_dict_for_marker(
            method_tp=method_tp,
            marker_tp=marker_tp,
            fields=marker_fields,
        )

    return MethodContext(
        types=types,
        fields=fields,
    )


def get_marker_fields(
    fields: Sequence[Field[Any]],
) -> Mapping[type[BaseMarker], Sequence[Field[Any]]]:
    result = defaultdict(list)

    for field in fields:
        marker_tp = get_marker_type(field.type)
        if marker_tp is not None:
            result[marker_tp].append(field)

    return result


def make_typed_dict_for_marker(
    method_tp: "type[Method[Any]]",
    marker_tp: type[BaseMarker],
    fields: Sequence[Field[Any]],
) -> Any | None:
    if not fields:
        return None

    name = f"{method_tp.__name__}{marker_tp.__name__}Type"

    fields_tp: MutableMapping[str, Any] = {}
    for field in fields:
        fields_tp[field.name] = field.type

    return TypedDict(name, fields_tp, total=False)  # type: ignore[operator]
