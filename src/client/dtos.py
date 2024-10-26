from pydantic import BaseModel


class CreateClientDto(BaseModel):
    name: str


class UpdateClientDto(BaseModel):
    id: int
    name: str