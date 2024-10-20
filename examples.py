from lunnarisweb.controller import Controller
from lunnarisweb.endpoint import get, post


def pre_middleware():
    print("Pre middleware")


def post_middleware(res):
    print("Post middleware: Upper")
    return res.upper()


class ExampleController(Controller):
    pre_middlewares = [pre_middleware]
    post_middlewares = [post_middleware]

    def __init__(self, service):
        self.service = service

    @get("/example")
    def get_example(self):
        return self.service()

    @post("/example")
    def post_example(self):
        return self.service()


def service():
    return "Hello, world!"


controller = ExampleController(service)

endpoints = controller.get_endpoints()

for endpoint in endpoints:
    res = endpoint()
    print(res)
