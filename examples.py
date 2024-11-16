from dataclasses import dataclass, is_dataclass, asdict
from lunnaris.application import Application, Serializer
from lunnaris.controller import Controller
from lunnaris.handler import get, post, put, delete
from lunnaris.request import Json
from lunnaris.exceptions import BadRequest, NotFound
from lunnaris import asgi


@dataclass(kw_only=True)
class ClientModel:
    id: int = None
    name: str
    age: int


class ClientService:
    clients: list[ClientModel] = []
    last_id: int = 0

    @classmethod
    def save(cls, data: ClientModel):
        cls.last_id += 1
        data.id = int(cls.last_id)
        cls.clients.append(data)
        return True

    @classmethod
    def all(cls):
        return cls.clients

    @classmethod
    def get(cls, id: int):
        for client in cls.clients:
            if client.id == id:
                return client
        return None

    @classmethod
    def delete(cls, id: int):
        for i, client in enumerate(cls.clients):
            if client.id == id:
                del cls.clients[i]
                return True
        return False

    @classmethod
    def update(cls, id: int, data: ClientModel):
        for i, client in enumerate(cls.clients):
            if client.id == id:
                data.id = id
                cls.clients[i] = data
                return True
        return False


def dataclass_serializer(data):
    print(data)
    if is_dataclass(data):
        return asdict(data), "application/json"
    if isinstance(data, dict):
        return data, "application/json"
    return str(data), "text/plain"


class ClientController(Controller):
    __route__ = "clients"

    def __init__(self, service: ClientService, **kwargs):
        super().__init__(**kwargs)
        self.service = service

    @post("", status_code=201)
    def create(self, data: ClientModel = Json()):
        if self.service.save(data):
            return "Client created", 201, {"x-api-key": "123"}
        raise BadRequest("Client already exists")

    @get("/{id}")
    def get_(self, id: int):
        client = self.service.get(id)
        if client:
            return client
        raise NotFound("Client not found")

    @get("")
    def all(self):
        return self.service.all()

    @put("{id}")
    def update(self, id: int, data: ClientModel = Json()):
        if self.service.update(id, data):
            return "Client updated"
        raise BadRequest("Error updating client")

    @delete("/{id}")
    def delete(self, id: int):
        if self.service.delete(id):
            return "Client deleted"
        raise NotFound("Client not found")


def run():
    app = Application(serializer=Serializer())
    app.container.add_dependency(ClientService)
    app.add_controller(ClientController)
    app.init()
    return asgi.create_asgi_app(app)
    