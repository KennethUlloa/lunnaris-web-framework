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
        headers: dict[str, str] = None,
        body: bytes | str | None = None,
        query: dict[str, str] = None,
        params: dict[str, str] = None,
    ):
        self.method = method
        self.path = path
        self.headers = MappingProxyType(headers or {})
        self.body = body
        self.query = MappingProxyType(query or {})
        self.params = MappingProxyType(params or {})

    def get_body(self):
        if self.method.lower() == Method.GET.lower():
            raise ValueError("GET request can't have a body")

        return self.body


class ITypeMapper(Generic[T], ABC):
    content_type: str

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def map(self, req: Request) -> T:
        pass

    def init_type(self, data: Any, type_: Type[T]) -> T:
        return type_(**data)


class ParamMapper(Generic[T], ABC):
    @abstractmethod
    def map(self, req: Request, type_: Type[T], param_name: str) -> T:
        pass


class Json(ITypeMapper[T]):
    content_type = MimeType.JSON.lower()

    def map(self, request: Request, type_: Type[T]) -> T:
        content_type: str = request.headers.get(Header.CONTENT_TYPE.lower(), "").lower()

        if self.content_type not in content_type:
            raise ValueError("Wrong mimetype for converter")

        body = request.get_body()

        if not body:
            raise ValueError("Empty body")

        return self.init_type(json.loads(body), type_)


class Query(ITypeMapper[T]):
    def __init__(self, default: dict[str, str] = {}):
        self.default = default

    def map(self, request: Request, type_: Type[T]) -> T:
        query_data = {**self.default}
        query_data.update(request.query)
        return type_(**query_data)


class QueryParam(ParamMapper[T]):
    def __init__(self, default=None) -> None:
        self.default = default

    def map(self, req: Request, type_: Type[T], param_name: str) -> T:
        if param_name not in req.query:
            if self.default is None:
                raise ValueError(f"Parameter {param_name} not found in request")
            if isinstance(self.default, type_):
                return self.default
            else:
                raise ValueError(f"Invalid default value for {param_name}")
        return type_(req.query[param_name])
