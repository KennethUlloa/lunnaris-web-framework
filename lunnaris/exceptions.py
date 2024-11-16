class HttpException(Exception):
    code: int
    title: str
    message: bytes | str

    def __init__(self, title: str, code: int, message: str) -> None:
        super().__init__(f"{code} - {title}")
        self.code = code
        self.title = title or f"{code} - {self.title}"
        self.message = message
    
    def __repr__(self) -> str:
        if self.message:
            return f"{self.code} - {self.title}: {self.message}"
        return f"{self.code} - {self.title}"

    def __str__(self) -> str:
        return self.__repr__()


class DefinedHttpException(HttpException):
    def __init__(self, body: str = ""):
        super().__init__(self.title, self.code, body)


class BadRequest(DefinedHttpException):
    code = 400
    title = "Bad request"


class Unauthorized(DefinedHttpException):
    code = 401
    title = "Unauthorized"


class Forbidden(DefinedHttpException):
    code = 403
    title = "Forbidden"


class NotFound(DefinedHttpException):
    code = 404
    title = "Not found"


class InternalServerError(DefinedHttpException):
    code = 500
    title = "Internal server error"


class NotImplemented(DefinedHttpException):
    code = 501
    title = "Not implemented"


class BadGateway(DefinedHttpException):
    code = 502
    title = "Bad gateway"
