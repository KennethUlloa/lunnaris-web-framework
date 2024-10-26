import json
from abc import ABC, abstractmethod
from types import MappingProxyType
from typing import Any, Type
from .enums import MimeType


class Request:
    method: str
    path: str
    headers: MappingProxyType[str, str]
    body: bytes | str | None
    query: MappingProxyType[str, str]
    params: MappingProxyType[str, str]

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


class ITypeMapper(ABC):
    def __init__(self, type_: Type, request: Request):
        if not type_:
            raise ValueError("type_ must not be None")

        if not request:
            raise ValueError("request must not be None")

        self.type_ = type_
        self.request = request

    @abstractmethod
    def map(self) -> Type:
        pass

    def init_type(self, data: Any):
        return self.type_(**data)


class Body(ITypeMapper):
    def map(self) -> Type:
        if MimeType.JSON in self.request.headers.get("content-type", ""):
            if not self.request.body:
                raise ValueError("Request body is empty")
            body = (
                self.request.body
                if isinstance(self.request.body, str)
                else str(self.request.body, "utf-8")
            )
            return self.init_type(json.loads(body))

        raise ValueError(
            f"Not supported content type: {self.request.headers.get('content-type')}"
        )


