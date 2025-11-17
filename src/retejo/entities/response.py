from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from typing_extensions import override

_RawResponseT = TypeVar("_RawResponseT")


class Response(ABC, Generic[_RawResponseT]):
    __slots__ = ("_raw_response",)

    def __init__(self, raw_response: _RawResponseT) -> None:
        self._raw_response = raw_response

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._raw_response!r})>"

    @property
    def raw_response(self) -> _RawResponseT:
        return self._raw_response

    @property
    @abstractmethod
    def raw_result(self) -> Any:
        raise NotImplementedError
