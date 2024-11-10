from .handler import PreMiddleware, PostMiddleware, get_handler, RequestHandler


class Controller:
    __route__ = None
    def __init__(self, pre_middlewares: list[PreMiddleware] = None, post_middlewares: list[PostMiddleware] = None) -> None:
        self.pre_middlewares = pre_middlewares or []
        self.post_middlewares = post_middlewares or []

    def get_handlers(self) -> list[RequestHandler]:
        endpoints = []
        for name, element in vars(self.__class__).items():
            ep = get_handler(element)
            if ep is not None:
                if self.__route__:
                    controller = self.__route__.strip("/")
                    path = ep.path.strip("/")
                    if controller and path:
                        path = f"/{controller}/{path}"
                    elif controller:
                        path = f"/{controller}"
                    ep.path = path
                ep.callback = getattr(self, name)
                ep.add_post_middlewares(self.post_middlewares, 'after')
                ep.add_pre_middlewares(self.pre_middlewares, 'before')
                endpoints.append(ep)
        return endpoints
