from typing import Any

from typing_extensions import override


class RetejoError(Exception):
    """Base retejo error."""


class IntegrationError(RetejoError):
    """
    Integration error.

    Called if an integration error has occurred.
    """


class UnmarkedFieldError(RetejoError):
    def __init__(
        self,
        method_name: Any,
        field_name: str,
    ) -> None:
        super().__init__(method_name, field_name)
        self.method_name = method_name
        self.field_name = field_name

    @override
    def __str__(self) -> str:
        return (
            f"Field `{self.method_name}.{self.field_name}` unmarked.\n"
            " * Use markers that are inherited from `BaseMarker`."
        )
