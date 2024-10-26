from inspect import signature
from typing import Callable, Literal, Any


from .request import Request, ITypeMapper
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
    path: str
    method: str
    callback: Callable
    status_code: int = 200
    headers: dict[str, str] = {}
    pre_middleware: list[PreMiddleware] = []
    post_middleware: list[PostMiddleware] = []

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

        if not req:
            raise ValueError("Request can't be none")
        
        return req
    
    def _process_post_middleware(self, response: Any) -> Any:
        res = response
        for middleware in self.post_middleware:
            temp = middleware(res)
            if temp:
                res = temp

        if not res:
            raise ValueError("Response can't be empty")
        
        return res
        

    
    def _process_callback_kwargs(self, request: Request) -> dict:
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
        
        return kwargs
    
    def add_pre_middlewares(self, middlewares: list[PreMiddleware], hint: Literal['before','after'] = 'before'):
        if hint == "before":
            middlewares.extend(self.pre_middleware)
            self.pre_middleware = middlewares
        else:
            self.pre_middleware.extend(middlewares)

    def add_post_middlewares(self, middlewares: list[PostMiddleware], hint: Literal['before','after'] = 'after'):
        if hint == "before":
            middlewares.extend(self.pre_middleware)
            self.post_middleware = middlewares
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
        ep = RequestHandler()
        ep.path = url
        ep.method = method
        ep.status_code = status_code
        ep.pre_middleware = pre_middleware
        ep.post_middleware = post_middleware
        ep.headers = headers
        ep.callback = func
        func.__handler__ = ep
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
    handler = getattr(obj, '__handler__', default)
    if isinstance(handler, RequestHandler):
        return handler
    else:
        return default
