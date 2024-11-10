import importlib
from functools import cache
from typing import Any, Callable, Type, Union, TypeVar
from inspect import signature

T = TypeVar("T")


@cache
def lazy_import(path):
    module_path, symbol_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, symbol_name)


class Lazy:
    def __init__(self, path: str) -> None:
        self.path = path

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return lazy_import(self.path)


class Dependency:
    def __init__(self, key: Union[Type[T], Callable], cached=False) -> None:
        self.key = key() if isinstance(key, Lazy) else key
        self.cached = cached
        self.annotations = {}
        self.defaults = {}
        self.cached_value = None

        for name, param in signature(key).parameters.items():
            if param.default != param.empty:  # Defaults before annotations
                self.defaults[name] = param.default
            elif param.annotation != param.empty:
                self.annotations[name] = param.annotation

    def __call__(self, *args: Any, **kwds: Any) -> T:
        if self.cached:
            if not self.cached_value:
                self.cached_value = self.key(*args, **kwds)
            return self.cached_value
        return self.key(*args, **kwds)


class Swappable(Dependency):
    def __init__(
        self, key: Union[Type, Callable], replace: Union[Type, Callable], cached=False
    ) -> None:
        super().__init__(replace, cached)
        self.key = key() if isinstance(key, Lazy) else key
        self.replace = replace() if isinstance(replace, Lazy) else replace

    def __call__(self, **kwds: Any) -> Any:
        if self.cached:
            if not self.cached_value:
                self.cached_value = self.replace(**kwds)
            return self.cached_value
        return self.replace(**kwds)


class DIContainer:
    def __init__(self) -> None:
        self.__dependencies: dict[Type, Dependency] = {}

    def add_dependency(
        self,
        dep: Union[Type, Callable],
        replace: Union[Type, Callable] = None,
        cached: bool = False,
    ):
        if replace:
            self.__dependencies[dep] = Swappable(dep, replace, cached)
        else:
            self.__dependencies[dep] = Dependency(dep, cached)

    def add(self, dep: Dependency):
        self.__dependencies[dep.key] = dep

    def resolve(self, key: Union[Type[T], Callable]) -> T:
        dep = self.__dependencies.get(key)
        if not dep:
            raise ValueError(f"Undefined dependency {dep}")

        if dep.cached and dep.cached_value:
            return dep.cached_value

        values = {}  # Parameters dictionary

        for name, val in dep.defaults.items():
            value = val
            if isinstance(val, Lazy):  # Defered import
                value = val()

            if callable(value):  # Inject the result of callables
                values[name] = (
                    self.resolve(value) if value in self.__dependencies else value()
                )
            else:
                values[name] = value

        for name, annotations in dep.annotations.items():
            values[name] = self.resolve(annotations)

        # obj = dep(**values)

        # if dep.cached:
        #    dep.cached_value = obj

        return dep(**values)
