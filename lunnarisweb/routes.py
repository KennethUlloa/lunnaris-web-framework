from .endpoint import Endpoint

class RouteNode:
    children: dict = {}
    is_terminal: bool = False
    param_name: str | None = None
    handler: dict[str, Endpoint] = {}


class RouteMatcher:
    root: RouteNode
    def __init__(self):
        self.root = RouteNode()

    def add_route(self, handler: Endpoint):
        current_node: RouteNode = self.root
        segments = handler.path.strip("/").split("/")

        for segment in segments:
            if segment.startswith("{") and segment.endswith("}"):
                param_name = segment[1:-1]
                if "{param}" not in current_node.children:
                    current_node.children["{param}"] = RouteNode()
                current_node = current_node.children["{param}"]
                current_node.param_name = param_name
            else:
                if segment not in current_node.children:
                    current_node.children[segment] = RouteNode()
                current_node = current_node.children[segment]

        current_node.is_terminal = True
        current_node.handler[handler.method] = handler

    def match(self, path: str, method: str):
        current_node: RouteNode = self.root
        segments = path.strip("/").split("/")
        params = {}

        for segment in segments:
            if segment in current_node.children:
                current_node = current_node.children[segment]
            elif "{param}" in current_node.children:
                current_node = current_node.children["{param}"]
                params[current_node.param_name] = segment
            else:
                return None

        if current_node.is_terminal and method in current_node.handler:
            return (
                current_node.handler[method],
                params,
            )  # Devolvemos la función asociada y los parámetros
        return None
