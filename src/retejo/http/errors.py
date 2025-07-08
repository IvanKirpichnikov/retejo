from retejo.core.errors import RetejoError, retejo_error


@retejo_error
class MalformedResponseError(RetejoError):
    """
    Malformed response error.

    Called if the response cannot be parsed.
    """


@retejo_error
class ClientError(RetejoError):
    """Client error."""

    status_code: int

    def __str__(self) -> str:
        return f"Client error with {self.status_code!r} error code"


@retejo_error
class ServerError(RetejoError):
    """Server error."""

    status_code: int

    def __str__(self) -> str:
        return f"Server error with {self.status_code!r} error code"
