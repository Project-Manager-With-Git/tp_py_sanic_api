from sanic import Sanic
from asyncio import AbstractEventLoopPolicy


def init_listeners(app: Sanic) -> Sanic:
    @app.listener("before_server_start")
    async def listener_1(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_1")

    @app.listener("before_server_start")
    async def listener_2(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_2")

    @app.listener("after_server_start")
    async def listener_3(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_3")

    @app.listener("after_server_start")
    async def listener_4(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_4")

    @app.listener("before_server_stop")
    async def listener_5(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_5")

    @app.listener("before_server_stop")
    async def listener_6(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_6")

    @app.listener("after_server_stop")
    async def listener_7(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_7")

    @app.listener("after_server_stop")
    async def listener_8(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        print("listener_8")
    return app
