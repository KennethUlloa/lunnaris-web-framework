from .request import Request
from .response import Response


def parse_query_string(query_string: str) -> dict[str, str]:
    query: dict[str, str] = {}
    for v in query_string.decode().split("&"):
        vals = v.split("=")
        if len(vals) == 2:
            key, value = vals
            query[key] = value
    
    return query


async def read_body(recieve) -> bytes:
    body = b''
    more_body = True

    while more_body:
        message = await recieve()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body


async def read_request(scope: dict, recieve) -> Request:
    if scope["type"] != "http":
        return

    return Request(
        method=scope["method"],
        path=scope["path"],
        headers={k.decode(): v.decode() for k, v in scope["headers"]},
        query=parse_query_string(scope["query_string"]),
        body=await read_body(recieve)
    )


async def send_response(response: Response, send) -> None:
    await send({
        "type": "http.response.start",
        "status": response.status_code,
        "headers": [
            [k.encode(), v.encode()]
            for k, v in response.headers.items()
        ],
    })

    await send({
        "type": "http.response.body",
        "body": response.body,
    })

def create_asgi_app(app):
    async def asgi_app(scope, recieve, send):
        req = await read_request(scope, recieve)
        res = app.run(req)
        await send_response(res, send)
    
    return asgi_app