from .types import Headers


class Response:
    def __init__(
        self,
        status_code: int,
        body: str | bytes,
        headers: dict[str, str] | Headers = None,
    ):
        self.status_code = status_code
        self.body = body if isinstance(body, bytes) else body.encode()
        if isinstance(headers, dict):
            self.headers = Headers(headers)
        elif isinstance(headers, Headers):
            self.headers = headers
        else:
            self.headers = Headers({"content-type": "text/html"})
