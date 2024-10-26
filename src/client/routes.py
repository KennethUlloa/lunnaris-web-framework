from fastapi import APIRouter
from .dtos import CreateClientDto, UpdateClientDto
from .services import all, find, create, update, delete


router = APIRouter(prefix="/client", tags=["Client"])


@router.post("/")
def create_client(data: CreateClientDto):
    return create(data)


@router.get("/")
def all_client():
    return all()


@router.get("/{id}")
def find_client(id: int):
    return find(id)


@router.put("/")
def update_client(data: UpdateClientDto):
    return update(data)


@router.delete("/{id}")
def delete_client(id: int):
    return delete(id)