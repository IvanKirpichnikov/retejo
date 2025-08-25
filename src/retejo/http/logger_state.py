from logging import getLogger

from retejo.core.logger_proto import LoggerProto

default_method_logger = getLogger("retejo.http.method")
default_response_logger = getLogger("retejo.http.response")
default_request_logger = getLogger("retejo.http.request")
default_curl_logger = getLogger("retejo.http.request.curl")


class HttpLoggerState:
    def __init__(
        self,
        method: LoggerProto = default_method_logger,
        response: LoggerProto = default_response_logger,
        request: LoggerProto = default_request_logger,
        curl: LoggerProto = default_curl_logger,
    ) -> None:
        self._method = method
        self._response = response
        self._request = request
        self._curl = curl

    @property
    def method(self) -> LoggerProto:
        return self._method

    @property
    def response(self) -> LoggerProto:
        return self._response

    @property
    def request(self) -> LoggerProto:
        return self._request

    @property
    def curl(self) -> LoggerProto:
        return self._curl
