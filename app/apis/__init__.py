from sanic import Sanic, Blueprint
from .usernamespace import usernamespace_v1

api = Blueprint.group(usernamespace_v1, url_prefix="/api")


def init_api(app: Sanic) -> Sanic:
    app.blueprint(api)
    return app
