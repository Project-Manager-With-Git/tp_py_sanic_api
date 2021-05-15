from typing import TypeVar, Optional
from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import BaseHTTPResponse
from sanic.blueprint_group import BlueprintGroup
from asyncio import AbstractEventLoopPolicy

T = TypeVar('T', Sanic, Blueprint, BlueprintGroup)


def init_middleware(instance: T) -> T:
    @instance.middleware("request")
    async def add_key(request: Request) -> Optional[BaseHTTPResponse]:
        # Arbitrary data may be stored in request context:
        request.ctx.foo = "bar"

    @instance.middleware("response")
    async def custom_banner(request: Request, response: BaseHTTPResponse) -> Optional[BaseHTTPResponse]:
        response.headers["Server"] = "Fake-Server"

    return instance
