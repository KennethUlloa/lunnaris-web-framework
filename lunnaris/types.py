class Headers:
    def __init__(self, headers: dict[str, str], frozen=False):
        self.__headers = {k.lower(): v for k, v in headers.items()}
        self.__frozen = frozen

    def __getitem__(self, key):
        return self.__headers[key.lower()]

    def __setitem__(self, key, value):
        if self.__frozen:
            raise TypeError("Headers are frozen")
        if not isinstance(value, str):
            raise TypeError(f"Header value must be a string, not {type(value).__name__}")
        if not isinstance(key, str):
            raise TypeError(f"Header key must be a string, not {type(key).__name__}")
        self.__headers[key.lower()] = value

    def __delitem__(self, key):
        if self.__frozen:
            raise TypeError("Headers are frozen")
        del self.__headers[key.lower()]

    def __iter__(self):
        return iter(self.__headers)

    def __len__(self):
        return len(self.__headers)

    def __repr__(self):
        return f"Headers({self.__headers})"

    def __str__(self):
        return str(self.__headers)

    def __eq__(self, other):
        if isinstance(other, Headers):
            return self.__headers == other.dict()
        if isinstance(other, dict):
            return self.__headers == {k.lower(): v for k, v in other.items()}
        return super().__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, key):
        return key.lower() in self.__headers

    def __bool__(self):
        return bool(self.__headers)

    def __hash__(self):
        return hash(self.__headers)

    def get(self, key, default=None):
        return self.__headers.get(key.lower(), default)

    def copy(self):
        return Headers(self.__headers.copy())
    
    def freeze(self):
        self.__frozen = True
    
    def dict(self):
        return self.__headers.copy()
    
    def items(self):
        return self.__headers.items()
    
    def keys(self):
        return self.__headers.keys()
    
    def values(self):
        return self.__headers.values()
    
    def clear(self):
        if self.__frozen:
            raise TypeError("Headers are frozen")
        self.__headers = {}
    
    def update(self, headers):
        if self.__frozen:
            raise TypeError("Headers are frozen")
        self.__headers.update(headers)