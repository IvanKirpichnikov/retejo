from adaptix import Chain, Provider, name_mapping

from retejo._internal.predicates.base import Pred
from retejo._internal.predicates.first_stack_element import FisrtStackElementChecker
from retejo._internal.predicates.origin_subclass import OriginSubclassLSC
from retejo._internal.providers.concat import concat_provider
from retejo.core.entities import SequenceResult


def mapping_header(
    predicate: Pred,
    key: str,
) -> Provider:
    return name_mapping(map=[(predicate, ("headers", key))])


def mapping_cookie(predicate: Pred, key: str) -> Provider:
    return name_mapping(map=[(predicate, ("cookies", key))])


def mapping_response_data() -> Provider:
    return concat_provider(
        name_mapping(
            OriginSubclassLSC(SequenceResult),
            map={"result": "data"},
            chain=Chain.LAST,
        ),
        name_mapping(
            map=[
                (
                    ~FisrtStackElementChecker(SequenceResult),
                    ("data", ...),
                ),
            ],
            chain=Chain.LAST,
        ),
    )
