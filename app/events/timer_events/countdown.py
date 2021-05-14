import uuid
import asyncio
from sanic.request import Request, json
from sanic.response import HTTPResponse


async def countdown(request: Request, seconds: int) -> HTTPResponse:
    channel_id = uuid.uuid4().hex
    eid = 0
    for i in range(seconds, 0, -1):
        await request.app.sse_send(event="countdown", event_id=str(eid), data=str(i), channel_id=channel_id)
        eid += 1
        await asyncio.sleep(1)
    return json({"status": "ok"})
