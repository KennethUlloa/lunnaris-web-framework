class HttpException(Exception):
    code: int
    title: str
    body: bytes | str

    def __init__(self, message: str, code: int, body: bytes | str) -> None:
        super().__init__(f"{code} - {message}")
        self.code = code
        self.message = message
        self.body = body


class DefinedHttpException(HttpException):
    def __init__(self, body: bytes | str = b""):
        super().__init__(self.message, self.code, body)


class BadRequest(DefinedHttpException):
    code = 400
    title = "Bad request"


class Unauthorized(DefinedHttpException):
    code = 401
    title = "Unauthorized"


class Forbidden(DefinedHttpException):
    code = 403


class NotFound(DefinedHttpException):
    code = 404
    title = "Resource not found"


class InternalServerError(DefinedHttpException):
    code = 500
    title = "Internal server error"


class NotImplemented(DefinedHttpException):
    code = 501
    title = "Not implemented"


class BadGateway(DefinedHttpException):
    code = 502
    title = "Bad gateway"
