from .models import User
from .dtos import CreateUserDto, UpdateUserDto

def all() -> list[User]:
    pass

def find(id: int) -> User:
    pass

def create(data: CreateUserDto) -> User:
    pass

def update(data: UpdateUserDto) -> User:
    pass

def delete(id: int) -> bool:
    pass