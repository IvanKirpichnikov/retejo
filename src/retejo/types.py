from dataclasses import dataclass
from typing import IO


@dataclass
class File:
    contents: str | IO[bytes] | None = None
    content_type: str | None = None
    filename: str | None = None
