from fastapi import APIRouter
from .dtos import CreateAuthDto, UpdateAuthDto
from .services import all, find, create, update, delete


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/")
def create_auth(data: CreateAuthDto):
    return create(data)


@router.get("/")
def all_auth():
    return all()


@router.get("/{id}")
def find_auth(id: int):
    return find(id)


@router.put("/")
def update_auth(data: UpdateAuthDto):
    return update(data)


@router.delete("/{id}")
def delete_auth(id: int):
    return delete(id)