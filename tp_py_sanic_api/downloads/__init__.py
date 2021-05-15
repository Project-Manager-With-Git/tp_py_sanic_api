from sanic import Sanic, Blueprint
from .tables import tables

downloads = Blueprint.group(tables, url_prefix="/downloads")


def init_downloads(app: Sanic) -> Sanic:
    app.blueprint(downloads)
    return app
