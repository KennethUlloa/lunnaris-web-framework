from .handler import PreMiddleware, PostMiddleware, get_handler


class Controller:
    __name__ = None
    pre_middlewares: list[PreMiddleware] = []
    post_middlewares: list[PostMiddleware] = []

    def get_handlers(self):
        endpoints = []
        for name, element in vars(self.__class__).items():
            ep = get_handler(element)
            if ep is not None:
                if self.__name__:
                    ep.path = f"/{self.__name__}{ep.path}"
                ep.callback = getattr(self, name)
                ep.add_post_middlewares(self.post_middlewares, 'after')
                ep.add_pre_middlewares(self.pre_middlewares, 'before')
                endpoints.append(ep)
        return endpoints
