from sanic import Blueprint
from .userlistsource import UserListSource
from .usersource import UserSource

usernamespace_v1 = Blueprint("user", url_prefix="/user", version=1)
usernamespace_v1.add_route(UserListSource.as_view(), "/")
usernamespace_v1.add_route(UserSource.as_view(), "/<uid:int>")
