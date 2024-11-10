from types import MappingProxyType
from typing import Any, Callable, Type
from .enums import Header
from .controller import Controller
from .routes import RouteMatcher
from .response import Response
from .request import Request
from .handler import RequestHandler, PostMiddleware, PreMiddleware, get_handler
from .exceptions import HttpException, NotFound, InternalServerError
from .serializer import Serializer


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
        self.exception_handlers = exception_handlers or {}
        self.pre_middlewares = pre_middlewares or []
        self.post_middlewares = post_middlewares or []

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
                raise NotFound(f"Resource {req.path} not found")

            handler, params = match
            req.params = MappingProxyType(params)
            response = handler(req)
            return self.handle_response(response, handler.status_code, handler.headers)
        except Exception as e:
            if not isinstance(e, HttpException):
                raise e
            
            status = InternalServerError.code
            message = str(InternalServerError())
            if isinstance(e, HttpException):
                status = e.code
                message = str(e)
                if e.body:
                    message += str(e.body)
            
            exception_type = type(e)
            if exception_type in self.exception_handlers:
                base = self.exception_handlers[exception_type](e)
                return self.handle_response(base, status, {})

            for t, h in self.exception_handlers.items():
                if isinstance(e, t):
                    return self.handle_response(h(e), status, {})

            message +=  f"\n{e.__class__.__name__}: {e}"
            
            return Response(
                status, message.encode(), {Header.CONTENT_TYPE: "text/plain"}
            )

    def handle_response(self, response, status, headers) -> Response:
        if isinstance(response, Response):
            return response
        body, content_type = self.serializer.serialize(response)
        print(body)
        body = body.encode()
        h = {**headers}
        if content_type:
            h[Header.CONTENT_TYPE] = content_type

        return Response(status, body, h)
