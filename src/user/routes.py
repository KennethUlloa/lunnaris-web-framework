from fastapi import APIRouter
from .dtos import CreateUserDto, UpdateUserDto
from .services import all, find, create, update, delete


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
def create_user(data: CreateUserDto):
    return create(data)


@router.get("/")
def all_user():
    return all()


@router.get("/{id}")
def find_user(id: int):
    return find(id)


@router.put("/")
def update_user(data: UpdateUserDto):
    return update(data)


@router.delete("/{id}")
def delete_user(id: int):
    return delete(id)