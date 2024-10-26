import json
from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, Type, Generic, TypeVar
from .enums import MimeType, Method, Header


T = TypeVar("T")


class Request:
    def __init__(
        self,
        method: str,
        path: str,
        headers: dict[str, str] = {},
        body: bytes | str | None = None,
        query: dict[str, str] = {},
        params: dict[str, str] = {},
    ):
        self.method = method
        self.path = path
        self.headers = MappingProxyType(headers)
        self.body = body
        self.query = MappingProxyType(query)
        self.params = MappingProxyType(params)

    def get_body(self):
        if self.method.lower() == Method.GET.lower():
            raise ValueError("GET request can't have a body")

        return self.body


class ITypeMapper(Generic[T], ABC):
    content_type: str

    def __init__(self, type_: Type[T]):
        self.type_ = type_

    @abstractmethod
    def map(self, req: Request) -> T:
        pass

    def init_type(self, data: Any):
        return self.type_(**data)
    

class Json(ITypeMapper[T]):
    content_type = MimeType.JSON.lower()

    def map(self, request: Request) -> T:
        content_type: str = request.headers.get(Header.CONTENT_TYPE.lower(), "").lower()

        if self.content_type not in content_type:
            raise ValueError("Wrong mimetype for converter")

        body = request.get_body()

        if not body:
            raise ValueError("Empty body")

        return self.init_type(json.loads(body))
