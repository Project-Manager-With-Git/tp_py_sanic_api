import asyncio
from datetime import datetime
from ..sse import sse


async def clock() -> None:
    while True:
        now = datetime.utcnow()
        now_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        await sse.send(event="time", data=now_str, channel_id="clock")
        await asyncio.sleep(1)
