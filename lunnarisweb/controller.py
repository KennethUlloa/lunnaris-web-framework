from .endpoint import Endpoint, PreMiddleware, PostMiddleware


def get_endpoint(obj):
    ep = getattr(obj, '__endpoint__', None)
    if not isinstance(ep, Endpoint):
        return None
    return ep


class Controller:
    __name__ = None
    pre_middlewares: list[PreMiddleware] = []
    post_middlewares: list[PostMiddleware] = []

    def get_endpoints(self):
        endpoints = []
        for name, element in vars(self.__class__).items():
            ep = get_endpoint(element)
            if ep is not None:
                ep.callback = getattr(self, name)
                ep.pre_middleware = self.pre_middlewares + ep.pre_middleware
                ep.post_middleware = ep.post_middleware + self.post_middlewares
                endpoints.append(ep)
        return endpoints
