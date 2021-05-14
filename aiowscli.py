import asyncio
from websockets import connect


async def main(url: str) -> None:
    async with connect(url) as websocket:
        await websocket.send("Hello world!")
        message = await websocket.recv()
        print(f"get message {message}")

asyncio.run(main("ws://localhost:5000/v1/ws/echo"))
