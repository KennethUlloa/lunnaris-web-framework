from lunnarisweb.application import WebApplication
from lunnarisweb.controller import Controller
from lunnarisweb.endpoint import get, post
from lunnarisweb.request import Body


def pre_middleware(req):
    print("Pre middleware: Params:", req.params)



def post_middleware(res):
    print("Post middleware: Upper")
    return res.upper()

class ClientModel:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class ExampleController(Controller):
    __name__ = "example"
    pre_middlewares = [pre_middleware]
    post_middlewares = [post_middleware]

    def __init__(self, service):
        self.service = service

    @post("", status_code=201)
    def get_example(self, data: ClientModel = Body):
        return self.service(data)

    @get("/{name}")
    def post_example(self, name: str):
        return f"Hello, {name}!"
    
    @get("/query")
    def get_query(self):
        return 


def service(data: ClientModel):
    return f"Hello, {data.name}! You are {data.age} years old."


app = WebApplication()
controller = ExampleController(service)

app.add_controller(controller)
