from asyncio import AbstractEventLoopPolicy
from sanic import Sanic
from pyloggerhelper import log
from tortoise.contrib.sanic import register_tortoise
from .usermodel import User

#"sqlite://:memory:"
def init_models(app: Sanic, db_url: str = "sqlite://database.db", generate_schemas: bool = True) -> Sanic:
    register_tortoise(
        app, db_url=db_url, modules={"models": ["models"]}, generate_schemas=generate_schemas
    )

    @app.listener("after_server_start")
    async def _(app: Sanic, loop: AbstractEventLoopPolicy) -> None:
        await User.init_Table()
    
    log.info("add user init_table to app")
    return app
