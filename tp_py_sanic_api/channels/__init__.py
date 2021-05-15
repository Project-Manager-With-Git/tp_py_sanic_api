from asyncio import AbstractEventLoopPolicy
from sanic import Sanic
from .sse import sse
from .trigger import trigger
from .backgrounds.clock import clock


def init_channels(app: Sanic) -> Sanic:
    sse.init_app(app, url="/channels")
    app.blueprint(trigger)

    @app.listener("after_server_start")
    async def _(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        await clock()
    return app
