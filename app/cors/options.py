from collections import defaultdict
from logging import setLoggerClass
from typing import Dict, FrozenSet, List
from sanic import Sanic, response
from sanic.request import Request
from sanic.router import Route
from .cors import _add_cors_headers


def _compile_routes_needing_options(routes: Dict[str, Route]) -> Dict[str, FrozenSet]:
    needs_options = defaultdict(list)
    # This is 21.3 and later. You will need to change this for older versions.
    for route in routes.values():
        for uri, methods in route.methods.items():
            if "OPTIONS" not in methods:
                needs_options[uri].extend(methods)
    return {
        uri: frozenset(methods) for uri, methods in dict(needs_options).items()
    }


def _options_wrapper(handler, methods, allow_credentials: bool = True,
                     allow_origin: List[str] = ["localhost"],
                     allow_header: List[str] = ["origin", "content-type", "accept", "authorization", "x-xsrf-token", "x-request-id"]):
    def wrapped_handler(request: Request, *args, **kwargs):
        nonlocal methods
        return handler(request, methods, allow_credentials=allow_credentials,
                       allow_origin=allow_origin,
                       allow_header=allow_header)

    return wrapped_handler


async def options_handler(request: Request, methods: List[str],
                          allow_credentials: bool = True,
                          allow_origin: List[str] = ["localhost"],
                          allow_header: List[str] = ["origin", "content-type", "accept", "authorization", "x-xsrf-token", "x-request-id"]) -> response.HTTPResponse:
    resp = response.empty()
    _add_cors_headers(resp, methods, allow_credentials=allow_credentials, allow_origin=allow_origin, allow_header=allow_header)
    return resp

def setup_options(app: Sanic, _: Any):
    app.router.reset()
    needs_options = _compile_routes_needing_options(app.router.routes_all)
    for uri, methods in needs_options.items():
        app.add_route(
            _options_wrapper(options_handler, methods),
            uri,
            methods=["OPTIONS"],
        )
    app.router.finalize()
