from types import MappingProxyType
from typing import Any, Callable, Type
from .enums import Header, MimeType
from .controller import Controller
from .routes import RouteMatcher
from .response import Response
from .request import Request
from .handler import RequestHandler, PostMiddleware, PreMiddleware
from .exceptions import NotFound
from .serializer import Serializer


class WebApplication:
    controllers: list[Controller]
    pre_middlewares: list[PreMiddleware] = []
    post_middlewares: list[PostMiddleware] = []
    router: RouteMatcher
    serializer: Serializer
    exception_handlers: dict[Type[Exception], Callable[[Exception], ]]

    def __init__(self):
        self.controllers = []
        self.router = RouteMatcher()
        self.serializer = Serializer()

    def add_controller(self, controller: Controller):
        for handler in controller.get_handlers():
            self.add_handler(handler)
    
    def add_handler(self, handler: RequestHandler):
        handler.add_pre_middlewares(self.pre_middlewares, 'before')
        handler.add_post_middlewares(self.post_middlewares, 'after')
        self.router.add_route(handler)


    async def run_async(self, req: Request) -> Response:
        try:
            match = self.router.match(req.path, req.method)

            if not match:
                raise NotFound(f"{req.path} could not be found")
            
            handler, params = match
            req.params = MappingProxyType(params)
            response = await handler(req)
            
            if isinstance(response, Response):
                return Response
            
            body = response
            status = handler.status_code
            headers = handler.headers

            if isinstance(response, tuple):
                if len(response) == 1:
                    body = response[0]

                elif len(response) == 2:
                    body = response[0]
                    status = response[1]
                
                elif len(response) >= 3:
                    body = response[0]
                    status = response[1]
                    headers = headers.update(response[2])
            
            if Header.CONTENT_TYPE not in headers:
                headers[Header.CONTENT_TYPE.lower()] = MimeType.UNKNOWN.lower()
            
            body = self.serializer.serialize(body)
            response = Response(status_code=status, body=body, headers=headers)
        except Exception as e:
            if type(e) in self.exception_handlers:
                base = self.exception_handlers[type](e)
                return self.handle_response(base)
            
            for t, h in self.exception_handlers.items():
                if isinstance(e, t):
                    return self.handle_response(h(e))
            
        
        return Response(500, b"Request couldn't be processed", {'content-type': 'text/plain; charset=utf-8'})

    def handle_response(self, response: Any, status=200, headers={}) -> Response:
        if isinstance(response, Response):
            return response    

        res = Response(status, b'')

        if isinstance(response, tuple):
            if len(response) == 1:
                body = response[0]

            elif len(response) == 2:
                body = response[0]
                res.status_code = response[1]
                
            elif len(response) >= 3:
                body = response[0]
                res.status_code = response[1]
                res.headers.update(response[2])
            
            res.body, content_type = self.serializer.serialize(body)
            
            if content_type:
                res.headers.update({Header.CONTENT_TYPE.lower():content_type.lower()})

            if Header.CONTENT_TYPE not in res.headers:
                res.headers.update({Header.CONTENT_TYPE.lower():MimeType.UNKNOWN.lower()})
            
            return res
