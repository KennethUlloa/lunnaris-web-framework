from typing import Callable


class Endpoint:
    url: str
    method: str
    callback: Callable
    status_code: int = 200


def endpoint(url: str, method: str, status_code: int = 200):
    def decorator(func):
        ep = Endpoint()
        ep.url = url
        ep.method = method
        ep.status_code = status_code
        ep.callback = func
        func.__endpoint__ = ep
        return func
    return decorator


def get(url):
    return endpoint(url, 'GET')

def post(url):
    return endpoint(url, 'POST')

def put(url):
    return endpoint(url, 'PUT')

def delete(url):
    return endpoint(url, 'DELETE')

def patch(url):
    return endpoint(url, 'PATCH')