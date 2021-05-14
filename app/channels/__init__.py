from sanic import Sanic
from .sse import sse
from .trigger import trigger
from .backgrounds.clock import clock


def init_channels(app: Sanic) -> Sanic:
    sse.init_app(app, url="/channels")
    app.blueprint(trigger)
    app.add_task(clock())
    return app
