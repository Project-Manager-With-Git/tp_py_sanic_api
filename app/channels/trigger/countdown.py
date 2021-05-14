import uuid
import asyncio
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json
from ..sse import sse, close_channel


async def countdown(request: Request, seconds: int) -> HTTPResponse:
    """启动一个倒计时频道.

    会返回一个channel_id,需要监听/channels?channel_id=<channel_id>才能获得倒计时数据
    """
    channel_id = uuid.uuid4().hex

    async def countdown_maker(seconds: int, channel_id: str) -> None:
        eid = 0
        for i in range(seconds, 0, -1):
            await sse.send(event="countdown", event_id=str(eid), data=str(i), channel_id=channel_id)
            eid += 1
            await asyncio.sleep(1)
        # close_channel(channel_id)

    app = request.app
    app.add_task(countdown_maker(seconds, channel_id))
    return json({"status": "ok", "channel_id": channel_id})
