from fastapi import APIRouter
from .dtos import Create{{ module.class_name }}Dto, Update{{ module.class_name }}Dto
from .services import all, find, create, update, delete


router = APIRouter(prefix="/{{ module.name }}", tags=["{{ module.class_name }}"])


@router.post("/")
def create_{{ module.name }}(data: Create{{ module.class_name }}Dto):
    return create(data)


@router.get("/")
def all_{{ module.name }}():
    return all()


@router.get("/{id}")
def find_{{ module.name }}(id: int):
    return find(id)


@router.put("/")
def update_{{ module.name }}(data: Update{{ module.class_name }}Dto):
    return update(data)


@router.delete("/{id}")
def delete_{{ module.name }}(id: int):
    return delete(id)
