from typing_extensions import override

from retejo.core.errors import RetejoError


class MalformedResponseError(RetejoError):
    """
    Malformed response error.

    Called if the response cannot be parsed.
    """


class ClientError(RetejoError):
    """Client error."""

    def __init__(self, status_code: int) -> None:
        super().__init__(status_code)
        self._status_code = status_code

    @override
    def __str__(self) -> str:
        return f"Client error with {self._status_code!r} error code"


class ServerError(RetejoError):
    """Server error."""

    def __init__(self, status_code: int) -> None:
        super().__init__(status_code)
        self._status_code = status_code

    @override
    def __str__(self) -> str:
        return f"Server error with {self._status_code!r} error code"
