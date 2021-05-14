from sanic import Blueprint
from sanic_sse import Sse
from .countdown import countdown

streams = Blueprint("streams", url_prefix="/streams", version=1)

streams.get("/countdown/<seconds:int>")(countdown)
