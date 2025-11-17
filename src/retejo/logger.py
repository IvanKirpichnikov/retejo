from abc import abstractmethod
from logging import getLogger
from typing import Any, Protocol

from typing_extensions import override

from retejo.entities.method import Method
from retejo.entities.request import Request
from retejo.entities.response import Response

default_method_logger = getLogger("retejo.method")
default_response_logger = getLogger("retejo.response")
default_request_logger = getLogger("retejo.request")


class Logger(Protocol):
    __slots__ = ()

    @abstractmethod
    def log_call_method(
        self,
        method: Method[Any],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def log_send_request(
        self,
        method: Method[Any],
        request: Request,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def log_receive_response(
        self,
        method: Method[Any],
        request: Request,
        response: Response[Any],
    ) -> None:
        raise NotImplementedError


class DefaultLogger(Logger):
    __slots__ = ()

    @override
    def log_call_method(
        self,
        method: Method[Any],
    ) -> None:
        method_class = method.__class__
        default_method_logger.debug(
            "Called method(%s.%s) ",
            method_class.__module__,
            method_class.__class__,
        )

    @override
    def log_send_request(
        self,
        method: Method[Any],
        request: Request,
    ) -> None:
        method_class = method.__class__
        default_method_logger.debug(
            "%s, %s",
            method_class.__module__,
            method_class.__class__,
        )

    @override
    def log_receive_response(
        self,
        method: Method[Any],
        request: Request,
        response: Response[Any],
    ) -> None:
        method_class = method.__class__
        default_method_logger.debug(
            "%s, %s",
            method_class.__module__,
            method_class.__class__,
        )


class EmptyLogger(Logger):
    __slots__ = ()

    @override
    def log_call_method(
        self,
        method: Method[Any],
    ) -> None: ...

    @override
    def log_send_request(
        self,
        method: Method[Any],
        request: Request,
    ) -> None: ...

    @override
    def log_receive_response(
        self,
        method: Method[Any],
        request: Request,
        response: Response[Any],
    ) -> None: ...
