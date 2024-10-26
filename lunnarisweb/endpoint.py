from inspect import signature
from typing import Callable, Any

from .response import Response
from .request import Request, ITypeMapper
from .enums import HttpMethod


# types
type PreMiddleware = Callable[[Request], None]
"""
PreMiddleware is a type alias for a callable that takes the request object and returns None.
If you need to break the chain of middlewares, you can raise an exception.
"""

type PostMiddleware = Callable[[Any], Any | Response]
"""
PostMiddleware is a type alias for a callable that takes one argument and returns it.
The argument and return type are the same. This is used to modify the response before it is sent.
"""


class Endpoint:
    path: str
    method: str
    callback: Callable
    status_code: int = 200
    headers: dict[str, str] = {}
    pre_middleware: list[PreMiddleware] = []
    post_middleware: list[PostMiddleware] = []

    def __call__(self, request: Request):
        for middleware in self.pre_middleware:
            middleware(request)
        kwargs = {}
        params = signature(self.callback).parameters

        for name, param in params.items():
            if issubclass(param.annotation, Request):
                kwargs[name] = request
            elif issubclass(param.default, ITypeMapper):
                type_mapper = param.default(param.annotation, request)
                kwargs[name] = type_mapper.map()
            else:
                arg = param.default
                if name in request.params:
                    arg = request.params[name]
                    if param.annotation != param.empty:
                        arg = param.annotation(arg)
                kwargs[name] = arg

        res = self.callback(**kwargs)
        for middleware in self.post_middleware:
            res = middleware(res)
        return res


def endpoint(
    url: str,
    method: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    def decorator(func):
        ep = Endpoint()
        ep.path = url
        ep.method = method
        ep.status_code = status_code
        ep.pre_middleware = pre_middleware
        ep.post_middleware = post_middleware
        ep.headers = headers
        ep.callback = func
        func.__endpoint__ = ep
        return func

    return decorator


def get(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return endpoint(
        url, HttpMethod.GET, status_code, pre_middleware, post_middleware, headers
    )


def post(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return endpoint(
        url, HttpMethod.POST, status_code, pre_middleware, post_middleware, headers
    )


def put(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return endpoint(
        url, HttpMethod.PUT, status_code, pre_middleware, post_middleware, headers
    )


def delete(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return endpoint(
        url, HttpMethod.DELETE, status_code, pre_middleware, post_middleware, headers
    )


def patch(
    url: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
    headers: dict[str, str] = {},
):
    return endpoint(
        url, HttpMethod.PATCH, status_code, pre_middleware, post_middleware, headers
    )
