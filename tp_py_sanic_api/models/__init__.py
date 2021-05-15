from sanic import Sanic
from pyloggerhelper import log
from tortoise.contrib.sanic import register_tortoise
from .usermodel import User


def init_models(app: Sanic, db_url: str = "sqlite://:memory:", generate_schemas: bool = True) -> Sanic:
    register_tortoise(
        app, db_url=db_url, modules={"models": ["tp_py_sanic_api.models"]}, generate_schemas=generate_schemas
    )
    app.add_task(User.init_Table())
    log.info("add user init_table to app")
    return app
