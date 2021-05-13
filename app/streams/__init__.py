from sanic import Blueprint
from .usersource import usersource_v1

stream = Blueprint.group(usersource_v1, url_prefix="/stream")