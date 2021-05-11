import functools
from typing import Callable, Any, Dict, Coroutine
from sanic.response import json, HTTPResponse
from sanic.request import Request
from jsonschema import validate


def checkjsonschema(schema: Dict[str, Any]) -> Callable[[Callable[..., Coroutine[Any, Any, HTTPResponse]]], Callable[..., Coroutine[Any, Any, HTTPResponse]]]:
    def decorate(func: Callable[..., Coroutine[Any, Any, HTTPResponse]]) -> Callable[..., Coroutine[Any, Any, HTTPResponse]]:
        @functools.wraps(func)
        async def wrap(request: Request, *args: Any, **kwargs: Any) -> HTTPResponse:
            query_json = request.json
            try:
                validate(instance=query_json, schema=schema)
            except Exception as e:
                return json({
                    "msg": "参数错误",
                    "error": str(e)
                }, status=401, ensure_ascii=False)
            else:
                response = await func(request, *args, **kwargs)
                return response
        return wrap
    return decorate
