from lunnarisweb.controller import Controller
from lunnarisweb.endpoint import get, post


class ExampleController(Controller):
    def __init__(self, service):
        self.service = service
    @get('/example')
    def get_example(self):
        return self.service()

    @post('/example')
    def post_example(self):
        return self.service()


def service():
    return 'Hello, world!'


controller = ExampleController(service)

endpoints = controller.get_endpoints()

for endpoint in endpoints:
    res = endpoint.callback()
    print(res)