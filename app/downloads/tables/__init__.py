from sanic import Blueprint
from .example_tables import example_tables

tables = Blueprint("tables", url_prefix="/tables", version=1)

tables.get("/example/<date:ymd>")(example_tables)
