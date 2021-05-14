from sanic import Sanic, Blueprint
from .echo import echo

ws = Blueprint("ws", url_prefix="/ws", version=1)

ws.add_websocket_route(echo, "/echo")


def init_ws(app: Sanic) -> Sanic:
    app.blueprint(ws)
    return app
