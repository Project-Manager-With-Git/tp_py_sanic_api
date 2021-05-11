
from functools import partial
from typing import List, Optional
from sanic import Sanic
from .cors import add_cors_headers
from .options import setup_options


def init_app(app: Sanic, *, allow_methods: Optional[List[str]] = None,
             allow_credentials: bool = True,
             allow_origin: List[str] = ["localhost"],
             allow_header: List[str] = ["origin", "content-type", "accept", "authorization", "x-xsrf-token", "x-request-id"]) -> Sanic:
    """为项目注册cros

    Args:
        app (Sanic): [description]

    Returns:
        Sanic: [description]
    """
    app.register_listener(partial(setup_options, allow_credentials=allow_credentials,
                                  allow_origin=allow_origin,
                                  allow_header=allow_header), "before_server_start")

    # Fill in CORS headers
    app.register_middleware(partial(add_cors_headers, allow_methods=allow_methods,
                                    allow_credentials=allow_credentials,
                                    allow_origin=allow_origin,
                                    allow_header=allow_header), "response")
