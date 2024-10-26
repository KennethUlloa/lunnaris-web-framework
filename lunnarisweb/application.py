from types import MappingProxyType
from .controller import Controller
from .routes import RouteMatcher
from .response import Response
from .asgi import read_request, send_response
from .serializer import Serializer


class WebApplication:
    controllers: list[Controller]
    router: RouteMatcher
    serializer: Serializer

    def __init__(self):
        self.controllers = []
        self.router = RouteMatcher()
        self.serializer = Serializer()

    def add_controller(self, controller: Controller):
        self.controllers.append(controller)
        for ep in controller.get_endpoints():
            self.router.add_route(ep)

    async def __call__(self, scope, receive, send):
        match = self.router.match(scope["path"], scope["method"].upper())
        if not match:
            response = Response(status_code=404, body=b"404 Not Found")
            await send_response(response, send)
            return
        endpoint, params = match
        request = await read_request(scope, receive)
        request.params = MappingProxyType(params)
        response = endpoint(request)
        
        if isinstance(response, Response):
            await send_response(response, send)
        
        body = response
        status = endpoint.status_code
        headers = endpoint.headers

        if "content-type" not in headers:
            headers["content-type"] = "text/plain"

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
        
        body = self.serializer.serialize(body)
        response = Response(status_code=status, body=body, headers=headers)
        await send_response(response, send)
     