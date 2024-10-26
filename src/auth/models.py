from pydantic import BaseModel


class Auth(BaseModel):
    id: int