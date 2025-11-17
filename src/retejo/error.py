from typing_extensions import override


class RetejoError(Exception): ...


class IntegrationError(RetejoError): ...


class UnmarkedFieldError(RetejoError):
    def __init__(
        self,
        method_cls: str,
        field_name: str,
    ) -> None:
        super().__init__(method_cls, field_name)
        self._method_cls = method_cls
        self._field_name = field_name

    @property
    def method_cls(self) -> type:
        return self.method_cls

    @property
    def field_name(self) -> str:
        return self._field_name

    @override
    def __str__(self) -> str:
        return (
            f"Field `{self.method_cls.__module__}:{self.method_cls.__qualname__}.{self._field_name}` unmarked.\n"
            " * Use markers that are inherited from `Marker`."
        )

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.method_cls}, {self.field_name})>"
