from sanic import Sanic, Blueprint
from sanic_sse import Sse
from .usersource import usersource_v1





events = Blueprint.group(usersource_v1, url_prefix="/events")


def init_events(app: Sanic) -> Sanic:
    Sse(sanic_app,url="/events")