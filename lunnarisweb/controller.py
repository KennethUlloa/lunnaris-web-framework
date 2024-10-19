from .endpoint import Endpoint


def get_endpoint(obj):
    ep = getattr(obj, '__endpoint__', None)
    if not isinstance(ep, Endpoint):
        return None
    return ep


class Controller:
    __name__ = None

    def get_endpoints(self):
        endpoints = []
        for name, element in vars(self.__class__).items():
            ep = get_endpoint(element)
            if ep is not None:
                ep.callback = getattr(self, name)
                endpoints.append(ep)
        return endpoints
