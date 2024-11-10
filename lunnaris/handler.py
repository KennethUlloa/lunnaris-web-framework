from inspect import signature
from typing import Callable, Literal, Any


from .request import ParamMapper, Request, ITypeMapper
from .enums import Method


# types
type PreMiddleware = Callable[[Request], Request]
"""
PreMiddleware is a type alias for a callable that takes the request object and returns None.
If you need to break the chain of middlewares, you can raise an exception.
"""

type PostMiddleware = Callable[[Any], Any]
"""
PostMiddleware is a type alias for a callable that takes one argument and returns it.
The argument and return type are the same. This is used to modify the response before it is sent.
"""


class RequestHandler:
    def __init__(
        self,
        path: str,
        method: str,
        callback: Callable,
        status_code: int = 200,
        headers: dict[str, str] = None,
        pre_middleware: list[PreMiddleware] = None,
        post_middleware: list[PostMiddleware] = None,
    ):
        self.path = path
        self.method = method
        self.callback = callback
        self.status_code = status_code
        self.headers = headers or {}
        self.pre_middleware = pre_middleware or []
        self.post_middleware = post_middleware or []

    def __call__(self, request: Request):
        req = self._process_pre_middleware(request)
        kwargs = self._process_callback_kwargs(req)
        res = self.callback(**kwargs)
        return self._process_post_middleware(res)

    def _process_pre_middleware(self, request: Request) -> Request:
        req = request

        for middleware in self.pre_middleware:
            temp = middleware(req)
            if temp:
                req = temp

        if req is None:
            raise ValueError("Request can't be none")

        return req

    def _process_post_middleware(self, response: Any) -> Any:
        res = response
        for middleware in self.post_middleware:
            temp = middleware(res)
            if temp:
                res = temp

        if res is None:
            raise ValueError("Response can't be empty")

        return res

    def _process_callback_kwargs(self, request: Request) -> dict:
        kwargs = {}
        params = signature(self.callback).parameters

        for name, param in params.items():
            if issubclass(param.annotation, Request):
                kwargs[name] = request
            elif isinstance(param.default, ITypeMapper):
                if param.annotation != param.empty:
                    kwargs[name] = param.default.map(request, param.annotation)
            elif isinstance(param.default, ParamMapper):
                if param.annotation != param.empty:
                    kwargs[name] = param.default.map(request, param.annotation, name)
            else:
                arg = param.default
                if name in request.params:
                    arg = request.params[name]
                    if param.annotation != param.empty:
                        arg = param.annotation(arg)
                kwargs[name] = arg

        return kwargs

    def add_pre_middlewares(
        self,
        middlewares: list[PreMiddleware],
        hint: Literal["before", "after"] = "before",
    ):
        if hint == "before":
            self.pre_middleware = middlewares + self.pre_middleware
        else:
            self.pre_middleware.extend(middlewares)

    def add_post_middlewares(
        self,
        middlewares: list[PostMiddleware],
        hint: Literal["before", "after"] = "after",
    ):
        if hint == "before":
            self.post_middleware = middlewares + self.post_middleware
        else:
            self.post_middleware.extend(middlewares)


def request_handler(
    url: str,
    method: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    def decorator(func):
        func.__handler__ = RequestHandler(
            url, method, func, status_code, headers, pre_middleware, post_middleware
        )
        return func

    return decorator


def get(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return request_handler(
        url, Method.GET, status_code, pre_middleware, post_middleware, headers
    )


def post(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return request_handler(
        url, Method.POST, status_code, pre_middleware, post_middleware, headers
    )


def put(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return request_handler(
        url, Method.PUT, status_code, pre_middleware, post_middleware, headers
    )


def delete(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return request_handler(
        url, Method.DELETE, status_code, pre_middleware, post_middleware, headers
    )


def patch(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return request_handler(
        url, Method.PATCH, status_code, pre_middleware, post_middleware, headers
    )


def get_handler(obj, default=None):
    handler = getattr(obj, "__handler__", default)
    if isinstance(handler, RequestHandler):
        return handler
    else:
        return default
