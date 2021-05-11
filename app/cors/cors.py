from typing import Iterable, List, Optional
from sanic.response import HTTPResponse
from sanic.request import Request


def _add_cors_headers(response: HTTPResponse, methods: Iterable[str],
                      allow_credentials: bool = True,
                      allow_origin: List[str] = ["localhost"],
                      allow_header: List[str] = ["origin", "content-type", "accept", "authorization", "x-xsrf-token", "x-request-id"]
                      ) -> None:
    allow_methods = list(set(methods))
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": ",".join(allow_methods),
        "Access-Control-Allow-Origin": ",".join(allow_origin),
        "Access-Control-Allow-Credentials": "true" if allow_credentials else "false",
        "Access-Control-Allow-Headers": ",".join(allow_header)
    }
    response.headers.extend(headers)


def add_cors_headers(request: Request, response: HTTPResponse, allow_methods: Optional[List[str]] = None,
                     allow_credentials: bool = True,
                     allow_origin: List[str] = ["localhost"],
                     allow_header: List[str] = ["origin", "content-type", "accept", "authorization", "x-xsrf-token", "x-request-id"]) -> None:
    if request.method != "OPTIONS":
        if allow_methods:
            methods = allow_methods
        else:
            methods = [method for methods in request.route.methods.values() for method in methods]
        _add_cors_headers(response, methods,
                          allow_credentials=allow_credentials,
                          allow_origin=allow_origin,
                          allow_header=allow_header)
