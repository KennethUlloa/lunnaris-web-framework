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
        self.router = router if router else RouteMatcher()
        self.serializer = serializer if serializer else Serializer()
        self.exception_handlers = exception_handlers if exception_handlers else {}
        self.pre_middlewares = pre_middlewares if pre_middlewares else []
        self.post_middlewares = post_middlewares if post_middlewares else []

    def add_controller(self, controller: Controller):
        for handler in controller.get_handlers():
            self.add_handler(handler)

    def add_handler(self, handler: RequestHandler):
        handler.add_pre_middlewares(self.pre_middlewares, "before")
        handler.add_post_middlewares(self.post_middlewares, "after")
        self.router.add_route(handler)

    def add_function_handler(self, handler: Callable):
        handler = get_handler(handler)
        if handler:
            self.add_handler(handler)
        else:
            raise ValueError("Invalid handler")

    def run(self, req: Request) -> Response:
        try:
            match = self.router.match(req.path, req.method)
            if not match:
                raise NotFound(f"Resource {req.path} not found")

            handler, params = match
            req.params = MappingProxyType(params)
            print("Handler headers", handler.headers)
            response = handler(req)
            return self.handle_response(response, handler.status_code, handler.headers)
        except Exception as e:
            print("Init exception")
            status = InternalServerError.code
            message = str(InternalServerError())
            if isinstance(e, HttpException):
                status = e.code
                message = str(e)
            
            exception_type = type(e)
            if exception_type in self.exception_handlers:
                print("Exception handler")
                base = self.exception_handlers[exception_type](e)
                print(base)
                return self.handle_response(base, status, {})

            for t, h in self.exception_handlers.items():
                if isinstance(e, t):
                    return self.handle_response(h(e), status, {})

            return Response(
                status, message.encode(), {Header.CONTENT_TYPE: "text/plain"}
            )

    def handle_response(self, response, status, headers) -> Response:
        if isinstance(response, Response):
            return response

        res = Response(status, b"")
        body, content_type = self.serializer.serialize(response)
        print(content_type)
        res.body = body.encode()
        res.headers.update(headers)
        res.headers[Header.CONTENT_TYPE] = content_type

        return res
