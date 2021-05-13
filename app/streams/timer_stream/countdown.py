import asyncio
from sanic import Blueprint
from .sseevent import SSEEvent


@app.route("/countdown")
async def countdown(request):
    response = await request.respond(content_type="text/event-stream")
    eid = 0
    for i in range(10, 0, -1):
        await response.send(str(SSEEvent(eid, str(i))))
        eid += 1
        await asyncio.sleep(1)
    await response.send(str(SSEEvent(eid, "0")), True)
    return response
