from dataclasses import dataclass
from typing import override


@dataclass
class RetejoError(Exception):
    pass


@dataclass
class MalformedResponseError(RetejoError):
    pass


@dataclass
class ClientLibraryError(RetejoError):
    pass


@dataclass
class ClientError(RetejoError, RuntimeError):
    status_code: int

    @override
    def __str__(self) -> str:
        return f"Client error with {self.status_code!r} error code"


@dataclass
class ServerError(RetejoError, RuntimeError):
    status_code: int

    @override
    def __str__(self) -> str:
        return f"Server error with {self.status_code!r} error code"
