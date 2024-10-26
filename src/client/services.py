from .models import Client
from .dtos import CreateClientDto, UpdateClientDto

client_data: list[Client] = []

def all() -> list[Client]:
    return client_data

def find(id: int) -> Client:
    for client in client_data:
        if client.id == id:
            return client
    return None

def create(data: CreateClientDto) -> Client:
    client = Client(
        id=len(client_data) + 1,
        name=data.name
    )
    client_data.append(client)
    return client

def update(data: UpdateClientDto) -> Client:
    for client in client_data:
        if client.id == data.id:
            client.name = data.name
            return client
    return None

def delete(id: int) -> bool:
    for client in client_data:
        if client.id == id:
            client_data.remove(client)
            return True
    return False