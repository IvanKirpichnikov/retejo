# https://github.com/reagento/dishka/blob/develop/src/dishka/entities/with_parents.py

import typing
from abc import ABC, ABCMeta
from collections.abc import Iterable
from enum import Enum
from itertools import chain
from typing import Final, Generic, Protocol

from retejo._internal._adaptix.common import TypeHint
from retejo._internal._adaptix.feature_requirement import (
    HAS_TV_TUPLE,
    HAS_UNPACK,
)
from retejo._internal._adaptix.type_tools import (  # type: ignore[attr-defined]
    normalize_type,
)
from retejo._internal._adaptix.type_tools.basic_utils import (
    get_type_vars_of_parametrized,
    is_generic,
    is_parametrized,
)
from retejo._internal._adaptix.type_tools.fundamentals import (
    get_generic_args,
    get_type_vars,
    strip_alias,
)
from retejo._internal._adaptix.type_tools.implicit_params import fill_implicit_params

IGNORE_TYPES: Final = (
    type,
    object,
    Enum,
    ABC,
    ABCMeta,
    Generic,
    Protocol,
    Exception,
    BaseException,
)

type TypeArgsTuple = tuple[TypeHint, ...]


def is_ignored_type(origin_type: TypeHint) -> bool:
    return origin_type in IGNORE_TYPES


class ParentsResolver:
    def get_parents(self, child_type: TypeHint) -> list[TypeHint]:
        if is_ignored_type(strip_alias(child_type)):
            raise ValueError(f"The starting class {child_type!r} is in ignored type")
        return list(self._resolve_parents(child_type))

    def _resolve_parents(self, tp: TypeHint) -> Iterable[TypeHint]:
        result = [tp]
        for parent in self._fetch_parents(tp):
            if not is_ignored_type(parent):
                result.extend(self._resolve_parents(parent))
        return result

    def _fetch_parents(self, tp: TypeHint) -> list[TypeHint]:
        if is_parametrized(tp):
            return self._get_parents_of_parametrized_generic(tp)
        if is_generic(tp):
            return self._get_parents_of_parametrized_generic(
                fill_implicit_params(tp),
            )
        return self._get_parents(tp)

    def _get_parents_of_parametrized_generic(
        self,
        parametrized_generic: TypeHint,
    ) -> list[TypeHint]:
        origin = strip_alias(parametrized_generic)
        type_var_to_actual = self._get_type_var_to_actual(
            get_type_vars(origin),
            self._unpack_args(get_generic_args(parametrized_generic)),
        )
        return [
            self._parametrize_by_dict(type_var_to_actual, tp) for tp in self._get_parents(origin)
        ]

    def _unpack_args(self, args: TypeArgsTuple) -> TypeArgsTuple:
        if HAS_UNPACK and any(strip_alias(arg) == typing.Unpack for arg in args):
            subscribed = tuple[args]  # type: ignore[valid-type]
            return tuple(arg.source for arg in normalize_type(subscribed).args)
        return args

    def _get_type_var_to_actual(
        self,
        type_vars: TypeArgsTuple,
        args: TypeArgsTuple,
    ) -> dict[TypeHint, TypeArgsTuple]:
        result = {}
        idx = 0
        for tv in type_vars:
            if HAS_TV_TUPLE and isinstance(tv, typing.TypeVarTuple):  # type: ignore[attr-defined, unused-ignore]
                tuple_len = len(args) - len(type_vars) + 1
                result[tv] = args[idx : idx + tuple_len]
                idx += tuple_len
            else:
                result[tv] = (args[idx],)
                idx += 1

        return result

    def _parametrize_by_dict(
        self,
        type_var_to_actual: dict[TypeHint, TypeArgsTuple],
        tp: TypeHint,
    ) -> TypeHint:
        params = get_type_vars_of_parametrized(tp)
        if not params:
            return tp
        return tp[
            tuple(
                chain.from_iterable(type_var_to_actual[type_var] for type_var in params),
            )
        ]

    def _get_parents(self, tp: TypeHint) -> list[TypeHint]:
        if hasattr(tp, "__orig_bases__"):
            return [
                parent
                for parent in tp.__orig_bases__
                if strip_alias(parent) not in (Generic, Protocol)
            ]
        return list(tp.__bases__)
