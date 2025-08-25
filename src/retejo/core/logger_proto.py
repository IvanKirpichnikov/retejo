from abc import abstractmethod
from collections.abc import Mapping
from types import TracebackType
from typing import Protocol, TypeAlias

_SysExcInfoType: TypeAlias = (
    tuple[
        type[BaseException],
        BaseException,
        TracebackType | None,
    ]
    | tuple[None, None, None]
)
_ExcInfoType: TypeAlias = None | bool | _SysExcInfoType | BaseException


class LoggerProto(Protocol):
    __slots__ = ()

    @abstractmethod
    def log(  # noqa: WPS211
        self,
        level: int,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        raise NotImplementedError
