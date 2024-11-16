from dataclasses import asdict, is_dataclass
import json
from typing import Type, Callable, Any, Union, Protocol


class ExtendedSerializer(Protocol):
    def match(self, obj: Any) -> bool:
        pass

    def serialize(self, obj: Any) -> Union[str, dict]:
        pass


SerializerCallback = Callable[[Any], Union[str, dict]]


class Serializer:
    def __init__(
        self,
        types: dict[Type, SerializerCallback] = None,
        extended_serializers: list[ExtendedSerializer] = None,
    ):
        self.__types: dict[Type, SerializerCallback] = types or {}
        self.extended_serializers = extended_serializers or []

    def serialize(self, obj: Any) -> tuple[str, str]:
        if isinstance(obj, list):
            return json.dumps([self._serialize_single(o) for o in obj]), "application/json"
        else:
            serialized = self._serialize_single(obj)
            if isinstance(serialized, (str, bytes, int, float, bool)):
                if isinstance(serialized, bytes):
                    serialized = serialized.decode()
                return str(serialized), "text/html"
            elif isinstance(serialized, dict):
                return json.dumps(serialized), "application/json"

        raise TypeError(f"Could not serialize {obj}")

    def add_serializer(self, t: Type, callback: SerializerCallback):
        print("Some type", t)
        self.__types[t] = callback

    def add_object_serializer(self, object_serializer: ExtendedSerializer):
        self.extended_serializers.append(object_serializer)

    def _serialize_single(self, obj: Any) -> Union[str, dict, int, float, bool]:
        if isinstance(obj, (str, dict, bytes, int, float, bool)):
            return obj  # Directly return primitive types without converting them to strings
        elif is_dataclass(obj):
            return asdict(obj)
        else:
            for obj_type, callback in self.__types.items():
                if isinstance(obj, obj_type):
                    serialized = callback(obj)
                    if isinstance(serialized, (str, dict)):
                        return serialized
            
            for extended_serializer in self.extended_serializers:
                if extended_serializer.match(obj):
                    result = extended_serializer.serialize(obj)
                    if isinstance(result, (str, dict)):
                        return result
                    
            raise TypeError(f"Could not serialize {obj}")

    def __str__(self) -> str:
        return str(self.__types)
