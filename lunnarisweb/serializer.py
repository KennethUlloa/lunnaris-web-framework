import json
from typing import Type, Callable, Any
from .enums import MimeType

type SerializerCallback = Callable[[Any], str|bytes]


class Serializer:
    types: dict[Type, SerializerCallback] = {}
    mimetypes: dict[Type, str] = {}

    def __init__(self):
        self.types = {
            str: lambda data, _: data,
            bytes: lambda data, _: data,
            int: lambda data, _: str(data),
            float: lambda data, _: str(data),
            dict: lambda data, _: json.dumps(data),
        }

        self.mimetypes = {
            str: MimeType.PLAIN,
            bytes: MimeType.UNKNOWN,
            int: MimeType.PLAIN,
            float: MimeType.PLAIN,
            dict: MimeType.JSON,
        }

    def add_type(self, type_: Type, mimetype: str, callback: SerializerCallback):
        self.types[type_] = callback
        self.mimetypes[type_] = mimetype

    def serialize(self, data: Any) -> str|bytes:
        if type(data) in self.types:
            return self.types[type(data)](data, self.types)
        
        for type_, callback in self.types.items():
            if isinstance(data, type_):
                return callback(data, self.types)
            
        raise ValueError(f"No serializer found for type {type(data)}")
