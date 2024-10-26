import json
from typing import Type, Callable, Any


type SerializerCallback = Callable[[Any], tuple[str, str]]


class Serializer:
    def __init__(self):
        self.__types: dict[Type, SerializerCallback] = {}
    
    def serialize(self, obj: Any) -> tuple[str, str]:
        if isinstance(obj, str):
            return obj, "text/html"
        
        if type(obj) in [int, float, bool]:
            return str(obj), "text/plain"

        if type(obj) in self.__types:
            print("here", obj)
            return self.__types[type(obj)](obj)
        
        for t, callback in self.__types.items():
            if isinstance(obj, t):
                return callback(obj)
        
        if isinstance(obj, dict):
            return json.dumps(obj), "application/json"
        
        if isinstance(obj, list):
            return json.dumps([self.serialize(i)[0] for i in obj]), "application/json"
        
        raise TypeError(f"Could not serialize {obj}")

    def add_serializer(self, t: Type, callback: SerializerCallback):
        self.__types[t] = callback

    def __str__(self) -> str:
        return str(self.__types)
