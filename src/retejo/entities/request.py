from typing_extensions import override

from retejo.entities.request_context_proxy import RequestContextProxy


class Request:
    __slots__ = ("_context",)

    def __init__(self, context: RequestContextProxy) -> None:
        self._context = context

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.context!r})>"

    @property
    def context(self) -> RequestContextProxy:
        return self._context
