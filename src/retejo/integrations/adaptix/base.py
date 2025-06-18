from typing import override

from adaptix import Retort, as_sentinel, name_mapping

from retejo.integrations.common.base import BaseClient, MarkersFactorties
from retejo.interfaces import Factory
from retejo.markers import (
    BodyMarker,
    HeaderMarker,
    Omitted,
    QueryParamMarker,
    UrlVarMarker,
)


class BaseAdaptixClient(BaseClient):
    @override
    def init_markers_factories(self) -> MarkersFactorties:
        retort = Retort(
            recipe=[
                as_sentinel(Omitted),
                name_mapping(
                    omit_default=True,
                ),
            ],
        )

        return {
            BodyMarker: retort,
            UrlVarMarker: retort,
            HeaderMarker: retort,
            QueryParamMarker: retort,
        }

    @override
    def init_response_factory(self) -> Factory:
        return Retort()
