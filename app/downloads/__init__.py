from sanic import Blueprint
from .tables import tables

downloads = Blueprint.group(tables, url_prefix="/downloads")