from pydantic import BaseModel


class Create{{ module.class_name }}Dto(BaseModel):
    pass


class Update{{ module.class_name }}Dto(BaseModel):
    id: int