from sanic import Blueprint
from sanic_sse import Sse
from .countdown import countdown

trigger = Blueprint("trigger", url_prefix="/trigger", version=1)

trigger.get("/countdown/<seconds:int>")(countdown)
