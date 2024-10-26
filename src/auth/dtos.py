from pydantic import BaseModel


class CreateAuthDto(BaseModel):
    pass


class UpdateAuthDto(BaseModel):
    id: int