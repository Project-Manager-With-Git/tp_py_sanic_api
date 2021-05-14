from sanic.request import Request
from sanic.websocket import WebSocketConnection
from sanic_openapi import doc

@doc.exclude(True)
async def echo(request: Request, ws: WebSocketConnection) -> None:
    while True:
        data = await ws.recv()
        if data:
            await ws.send(data)
            print(f'Received: {data}')
