from dataclasses import dataclass
from typing import IO


@dataclass(slots=True, frozen=True)
class FileObj:
    contents: str | bytes | IO[bytes]
    content_type: str | None = None
    filename: str | None = None
