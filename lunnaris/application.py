from types import MappingProxyType
from typing import Any, Callable, Type
from .enums import Header
from .controller import Controller
from .routes import RouteMatcher
from .response import Response
from .request import Request
from .handler import RequestHandler, PostMiddleware, PreMiddleware, get_handler
from .exceptions import HttpException, NotFound
from .serializer import Serializer


def exception_handler(e: Exception) -> Response:
    body = f"500 - Internal Server Error: {e.__class__.__name__}({str(e)})"
    return Response(500, body, {Header.CONTENT_TYPE: "text/plain"})


def handle_http_exception(e: HttpException) -> Response:
    return Response(e.code, str(e), {Header.CONTENT_TYPE: "text/plain"})


class Application:
    def __init__(
        self,
        router: RouteMatcher = None,
        serializer: Serializer = None,
        exception_handlers: dict[Type[Exception], Callable[[Exception], Any]] = None,
        pre_middlewares: list[PreMiddleware] = None,
        post_middlewares: list[PostMiddleware] = None,
    ):
        self.router = router or RouteMatcher()
        self.serializer = serializer or Serializer()
        self.pre_middlewares = pre_middlewares or []
        self.post_middlewares = post_middlewares or []
        self.exception_handlers = {
            **{
                HttpException: handle_http_exception,
            },
            **(exception_handlers or {}),
        }

    def add_exception_handler(self, t: Type, callback: Callable):
        self.exception_handlers[t] = callback

    def add_controller(self, controller: Controller):
        for handler in controller.get_handlers():
            self.add_handler(handler)

    def add_handler(self, handler: RequestHandler):
        handler.add_pre_middlewares(self.pre_middlewares, "before")
        handler.add_post_middlewares(self.post_middlewares, "after")
        self.router.add_route(handler)

    def add_function_handler(self, handler: Callable):
        handler: RequestHandler | None = get_handler(handler, None)
        if handler is None:
            raise ValueError("Invalid handler")
        self.add_handler(handler)

    def run(self, req: Request) -> Response:
        try:
            match = self.router.match(req.path, req.method)
            if not match:
                raise NotFound(f"Path {req.path} not found")

            handler, params = match
            req.params = MappingProxyType(params)
            return self.handle_response(handler(req))
        except Exception as e:
            return self.handle_exception(e)

    def handle_response(self, response, status=200, headers={}) -> Response:
        if isinstance(response, Response):
            return response

        c_status = status
        c_headers = headers
        c_body = response

        if isinstance(response, tuple):
            if len(response) == 2:
                c_body, c_status = response
            elif len(response) == 3:
                c_body, c_status, _headers = response
                c_headers.update(_headers)

        c_body, content_type = self.serializer.serialize(c_body)
        c_headers[Header.CONTENT_TYPE] = content_type
        return Response(c_status, c_body, c_headers)

    def handle_exception(self, e: Exception) -> Response:
        for t, callback in self.exception_handlers.items():
            if isinstance(e, t):
                return self.handle_response(
                    callback(e), 500, {Header.CONTENT_TYPE: "text/plain"}
                )
        return exception_handler(e)
