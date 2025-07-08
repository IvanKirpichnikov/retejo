from dataclasses import dataclass
from typing import TypeVar

from typing_extensions import dataclass_transform

_RetejoErrorClsT = TypeVar("_RetejoErrorClsT", bound="RetejoError", covariant=True)


@dataclass_transform(frozen_default=True)
def retejo_error(cls: type[_RetejoErrorClsT]) -> type[_RetejoErrorClsT]:
    return dataclass(
        frozen=True,
        slots=True,
    )(cls)


@retejo_error
class RetejoError(Exception):
    """Base retejo error."""


@retejo_error
class IntegrationError(RetejoError):
    """
    Integration error.

    Called if an integration error has occurred.
    """
