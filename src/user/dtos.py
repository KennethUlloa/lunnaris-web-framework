from pydantic import BaseModel


class CreateUserDto(BaseModel):
    pass


class UpdateUserDto(BaseModel):
    id: int