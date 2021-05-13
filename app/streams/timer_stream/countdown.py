import asyncio
from sanic.request import Request
from sanic.response import HTTPResponse
from .sseevent import SSEEvent


async def countdown(request: Request, seconds: int) -> HTTPResponse:
    response = await request.respond(content_type="text/event-stream")
    eid = 0
    for i in range(seconds, 0, -1):
        await response.send(str(SSEEvent(eid, str(i))))
        eid += 1
        await asyncio.sleep(1)
    await response.send(str(SSEEvent(eid, "0")), True)
    return response
