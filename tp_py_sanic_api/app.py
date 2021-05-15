import ssl
from typing import Any, Dict
from pyloggerhelper import log
from schema_entry import EntryPoint
from sanic import Sanic
from sanic_openapi import openapi2_blueprint
from .apis import init_api
from .downloads import init_downloads
from .channels import init_channels
from .ws import init_ws
from .listeners import init_listeners
from .middlewares import init_middleware
from .models import init_models


def new_app(config: Dict[str, Any]) -> Sanic:
    app_name = config.get("app_name", __name__)
    log_level = config.get("log_level")
    log.initialize_for_app(
        app_name=app_name,
        log_level=log_level
    )
    log.info("获取任务配置", config=config)
    sanic_app = Sanic(app_name)
    # 注册测试
    if config.get("debug"):
        from sanic_testing import TestManager
        TestManager(sanic_app)

    # 注册配置
    sanic_app.config.FALLBACK_ERROR_FORMAT = "json"
    # 注册插件
    # 注册静态文件
    if config.get("static_page_dir"):
        sanic_app.static("/", config["static_page_dir"])
    if config.get("static_source_dir"):
        sanic_app.static("/static", config["static_source_dir"])
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


def run_app(app: Sanic, config: Dict[str, Any]) -> None:
    # 启动
    host, port = config["address"].split(":")
    conf = {
        "host": host,
        "port": int(port),
        "workers": config.get("worker", 1),
        "debug": config.get("debug", True),
        "access_log": config.get("access_log", True),
    }
    # ssl相关配置
    if config.get("server_cert_path") and config.get("server_key_path"):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(config["server_cert_path"], keyfile=config["server_key_path"])
        if config.get("ca_cert_path"):
            context.load_verify_locations(config["ca_cert_path"])
            context.verify_mode = ssl.CERT_REQUIRED
            if config.get('client_crl_path'):
                context.load_verify_locations(config['client_crl_path'])
                context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
            log.info("use TLS with client auth")
        else:
            log.info("use TLS")
        conf["ssl"] = context
    app.run(**conf)


class Application(EntryPoint):
    """jsonrpc项目的服务端启动入口."""
    _name = "tp_py_sanic_api"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["address", "log_level"],
        "properties": {
            "app_version": {
                "type": "string",
                "title": "v",
                "description": "应用版本",
                "default": "0.0.0"
            },
            "app_name": {
                "type": "string",
                "title": "n",
                "description": "应用名",
                "default": "tp_py_sanic_api"
            },
            "address": {
                "type": "string",
                "title": "a",
                "description": "服务启动地址",
                "default": "0.0.0.0:5000"
            },
            "log_level": {
                "type": "string",
                "title": "l",
                "description": "log等级",
                "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
                "default": "DEBUG"
            },
            "static_page_dir": {
                "type": "string",
                "description": "静态网页文件路径",
            },
            "static_source_dir": {
                "type": "string",
                "description": "静态资源文件路径",
            },
            "debug": {
                "type": "boolean",
                "description": "是否使用debug模式运行程序",
                "default": True
            },
            "access_log": {
                "type": "boolean",
                "description": "是否运行程序时打印访问log",
                "default": True
            },
            "workers": {
                "type": "integer",
                "description": "是否多实例执行程序",
                "default": 1
            },
            "server_cert_path": {
                "type": "string",
                "description": "使用TLS时服务端的证书位置,如果为空则不适用TLS",
            },
            "server_key_path": {
                "type": "string",
                "description": "使用TLS时服务端证书的私钥位置",
            },
            "ca_cert_path": {
                "type": "string",
                "description": "使用TLS时的签发机构证书,如果为空则不使用客户端验证",
            },
            "client_crl_path": {
                "type": "string",
                "description": "使用TLS客户端验证时的客户端权限吊销列表路劲",
            }
        }
    }

    def do_main(self) -> None:
        app = new_app(self.config)
        run_app(app, self.config)
