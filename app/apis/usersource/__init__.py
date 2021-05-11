from sanic import Blueprint
from .userlistsource import UserListSource
from .usersource import UserSource

usersource_v1 = Blueprint("user", url_prefix="/user", version=1)
usersource_v1.add_route(UserListSource.as_view(), "/")
usersource_v1.add_route(UserSource.as_view(), "/<uid:int>")