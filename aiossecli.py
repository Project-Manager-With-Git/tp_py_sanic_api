import asyncio
import aiohttp
from aiohttp_sse_client import client as sse_client


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:5000/v1/trigger/countdown/15') as resp:
            resj = await resp.json()
            channel_id = resj.get("channel_id")
    async with sse_client.EventSource(f'http://localhost:5000/channels?channel_id={channel_id}') as event_source:
        try:
            async for event in event_source:
                print(event)
        except ConnectionError:
            pass


asyncio.run(main())
