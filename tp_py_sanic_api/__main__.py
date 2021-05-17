import ssl
import json
from pathlib import Path
from typing import Any, Dict
from pyloggerhelper import log
from sanic import Sanic
from sanic_openapi import openapi2_blueprint
from .apis import init_api
from .downloads import init_downloads
from .channels import init_channels
from .ws import init_ws
from .listeners import init_listeners
from .middlewares import init_middleware
from .models import init_models


def new_app() -> Sanic:
    config = {}
    configfilep = Path("config.json")
    if configfilep.is_file():
        with open(configfilep) as f:
            config = json.load(f)

    app_name = config.get("APP_NAME", __name__)
    sanic_app = Sanic(app_name, load_env=f'{app_name.upper()}_')
    sanic_app.update_config(config)
    log_level = sanic_app.config.get("LOG_LEVEL", "DEBUG")
    log.initialize_for_app(
        app_name=app_name,
        log_level=log_level
    )
    log.info("获取配置", config=sanic_app.config)

    # 注册测试
    if sanic_app.config.get("DEBUG", True):
        from sanic_testing import TestManager
        TestManager(sanic_app)

    # 注册配置
    sanic_app.config.FALLBACK_ERROR_FORMAT = "json"
    # 注册插件
    # 注册静态文件
    if sanic_app.config.get("static_page_dir"):
        sanic_app.static("/", sanic_app.config["static_page_dir"])
    if sanic_app.config.get("static_source_dir"):
        sanic_app.static("/static", sanic_app.config["static_source_dir"])
    # 注册蓝图
    sanic_app.blueprint(openapi2_blueprint)
    # 注册数据模型
    init_models(sanic_app)
    # 注册listeners
    init_listeners(sanic_app)
    # 注册中间件
    init_middleware(sanic_app)
    # 注册restful接口
    init_api(sanic_app)
    # 注册下载接口
    init_downloads(sanic_app)
    # 注册基于sse的channels
    init_channels(sanic_app)
    # 注册websocket
    init_ws(sanic_app)
    return sanic_app


app = new_app()
address = app.config.get("ADDRESS", "localhost:5000")
host, port = address.split(":")
conf = {
    "host": host,
    "port": int(port),
    "workers": app.config.get("WORKERS", 1),
    "debug": app.config.get("DEBUG", True),
    "access_log": app.config.get("ACCESSS_LOG", True),
}
# ssl相关配置
if app.config.get("SERV_CERT_PATH") and app.config.get("SERV_KEY_PATH"):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain(app.config["SERV_CERT_PATH"], keyfile=app.config["SERV_KEY_PATH"])
    if app.config.get("CA_CERT_PATH"):
        context.load_verify_locations(app.config["CA_CERT_PATH"])
        context.verify_mode = ssl.CERT_REQUIRED
        if app.config.get('CLIENT_CRL_PATH'):
            context.load_verify_locations(app.config['CLIENT_CRL_PATH'])
            context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
        log.info("use TLS with client auth")
    else:
        log.info("use TLS")
    conf["ssl"] = context
app.run(**conf)
