# type: ignore
from abc import abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Any, ClassVar, Protocol

from typing_extensions import Self

from retejo.core import Method
from retejo.core.clients.sync import SyncClient
from retejo.core.entities import Request, RequestContextProxy, Response


@dataclass
class ViewRequest:
    data: dict[str, Any]


@dataclass
class ViewResponse:
    data: dict[str, Any]


class View(Protocol):
    @abstractmethod
    def execute(self, request: ViewRequest) -> ViewResponse:
        raise NotImplementedError


class GetIntView(View):
    def execute(self, request: ViewRequest) -> ViewResponse:
        return ViewResponse(data={"result": 1})


class TestMethod(Method[ViewResponse]):
    view: ClassVar[type[View]]


class TestGetIntView(TestMethod):
    view = GetIntView



class TestRequest(Request):
    __slots__ = ("_data",)

    def __init__(
        self,
        data: dict[str, Any],
        context: RequestContextProxy,
    ) -> None:
        super().__init__(context)
        self._data = data

    @property
    def data(self) -> dict[str, Any]:
        return self._data


class TestResponse(Response):
    __slots__ = ("_data",)

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__()
        self._data = data

    @property
    def data(self) -> dict[str, Any]:
        return self._data


class TestClient(SyncClient[TestMethod, TestRequest, TestResponse]):
    __slots__ = ()

    def send_method(self, method: TestMethod) -> Response:
        self.handle_method(method)


    def handle_method(self, method: TestMethod) -> None:
        return None

    def send_request(
        self,
        request: TestRequest,
    ) -> TestResponse:
        return None

    def handle_request(
        self,
        request: TestRequest,
    ) -> None:
        return None

    def handle_response(
        self,
        response: TestResponse,
    ) -> None:
        return None

    def handle_error_response(self, response: TestResponse) -> None:
        return None

    def close(self) -> None:
        return None

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
