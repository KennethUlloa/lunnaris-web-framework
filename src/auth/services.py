from .models import Auth
from .dtos import CreateAuthDto, UpdateAuthDto

def all() -> list[Auth]:
    pass

def find(id: int) -> Auth:
    pass

def create(data: CreateAuthDto) -> Auth:
    pass

def update(data: UpdateAuthDto) -> Auth:
    pass

def delete(id: int) -> bool:
    pass