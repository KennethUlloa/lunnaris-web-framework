from .models import {{ module.class_name }}
from .dtos import Create{{ module.class_name }}Dto, Update{{ module.class_name }}Dto

def all() -> list[{{ module.class_name }}]:
    pass

def find(id: int) -> {{ module.class_name }}:
    pass

def create(data: Create{{ module.class_name }}Dto) -> {{ module.class_name }}:
    pass

def update(data: Update{{ module.class_name }}Dto) -> {{ module.class_name }}:
    pass

def delete(id: int) -> bool:
    pass
