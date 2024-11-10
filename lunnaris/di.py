from typing import Callable, Type, Union, TypeVar
from inspect import signature

T = TypeVar("T")


class Dependency:
    def __init__(self, key: Union[Type, Callable], cached = False) -> None:
        self.key = key
        self.cached = cached
        self.annotations = {}
        self.defaults = {}
        self.cached_value = None

        for name, param in signature(key).parameters.items():
            if param.default != param.empty: # Defaults before annotations
                self.defaults[name] = param.default
            elif param.annotation != param.empty:
                self.annotations[name] = param.annotation


class DIContainer:
    def __init__(self) -> None:
        self.__dependencies: dict[Type, Dependency] = {}

    def register(self, dep: Union[Type, Callable], cached = False):
        self.__dependencies[dep] = Dependency(dep, cached)

    def resolve(self, key: Union[Type[T], Callable]) -> T:
        dep = self.__dependencies.get(key)
        if not dep:
            raise ValueError('Undefined dependency')
        
        if dep.cached and dep.cached_value:
            return dep.cached_value
        
        values = {}

        for name, val in dep.defaults.items():
            if callable(val):
                values[name] = self.resolve(val) if val in self.__dependencies else val()
            else:
                values[name] = val
        
        for name, annotations in dep.annotations.items():
            values[name] = self.resolve(annotations)
        
        obj = dep.key(**values)
        
        if dep.cached:
            dep.cached_value = obj

        return obj
