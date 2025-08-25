from typing import Any

from adaptix import Loader, Mediator, Provider
from adaptix._internal.morphing.generic_provider import TypeHintTagsUnwrappingProvider
from adaptix._internal.morphing.request_cls import LoaderRequest
from adaptix._internal.provider.location import TypeHintLoc
from typing_extensions import override


class _FixedTypeHintTagsUnwrappingProvider(TypeHintTagsUnwrappingProvider):
    @override
    def _provide_proxy(self, mediator: Mediator[Any], request: LoaderRequest) -> Loader[Any]:
        return mediator.mandatory_provide(
            request.with_loc_stack(
                request.loc_stack.append_with(
                    TypeHintLoc(self._get_proxy_target(request.loc_stack.last.type))
                ),
            ),
            lambda provide: self._get_error_text(),
        )


def fixed_type_hint_tags_unwrapping_provider() -> Provider:
    return _FixedTypeHintTagsUnwrappingProvider()
