class Response:
    def __init__(
        self,
        status_code: int,
        body: str | bytes,
        headers: dict[str, str] = None,
    ):
        self.status_code = status_code
        self.body = body if isinstance(body, bytes) else body.encode()
        self.headers = headers or {"Content-Type": "text/html"}
