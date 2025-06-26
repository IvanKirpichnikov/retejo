from adaptix import Retort, as_sentinel

from retejo.integrations.adaptix._omit_provider import OmitOmittedFieldProvider
from retejo.integrations.common.base import BaseClient, MarkersFactorties
from retejo.markers.body import BodyMarker
from retejo.markers.header import HeaderMarker
from retejo.markers.omitted import Omitted
from retejo.markers.query_param import QueryParamMarker
from retejo.markers.url_var import UrlVarMarker


class BaseAdaptixClient(BaseClient[Retort]):
    def init_markers_factories(self) -> MarkersFactorties[Retort]:
        retort = Retort(
            recipe=[
                as_sentinel(Omitted),
                OmitOmittedFieldProvider(),
            ],
        )

        return {
            BodyMarker: retort,
            UrlVarMarker: retort,
            HeaderMarker: retort,
            QueryParamMarker: retort,
        }

    def init_response_factory(self) -> Retort:
        return Retort()
