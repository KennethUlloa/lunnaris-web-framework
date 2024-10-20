from typing import Callable, Any


# types
type PreMiddleware = Callable[[], None]
"""
PreMiddleware is a type alias for a callable that takes no arguments and returns None.
If you need to break the chain of middlewares, you can raise an exception.
"""

type PostMiddleware = Callable[[Any], Any]
"""
PostMiddleware is a type alias for a callable that takes one argument and returns it.
The argument and return type are the same. This is used to modify the response before it is sent.
"""


class Endpoint:
    url: str
    method: str
    callback: Callable
    status_code: int = 200
    pre_middleware: list[PreMiddleware] = []
    post_middleware: list[PostMiddleware] = []

    def __call__(self, *args, **kwargs):
        for middleware in self.pre_middleware:
            middleware()
        res = self.callback(*args, **kwargs)
        for middleware in self.post_middleware:
            res = middleware(res)
        return res


def endpoint(
    url: str,
    method: str,
    status_code: int = 200,
    pre_middleware: list[PreMiddleware] = [],
    post_middleware: list[PostMiddleware] = [],
):
    def decorator(func):
        ep = Endpoint()
        ep.url = url
        ep.method = method
        ep.status_code = status_code
        ep.pre_middleware = pre_middleware
        ep.post_middleware = post_middleware
        ep.callback = func
        func.__endpoint__ = ep
        return func

    return decorator


def get(url):
    return endpoint(url, "GET")


def post(url):
    return endpoint(url, "POST")


def put(url):
    return endpoint(url, "PUT")


def delete(url):
    return endpoint(url, "DELETE")


def patch(url):
    return endpoint(url, "PATCH")
