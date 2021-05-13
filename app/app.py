import ssl
from sanic import Sanic
from pyloggerhelper import log
from schema_entry import EntryPoint
from apis import api
from listeners import init_listeners
from middlewares import init_middleware


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
        app_name = self.config.get("app_name", __name__)
        log_level = self.config.get("log_level")
        log.initialize_for_app(
            app_name=app_name,
            log_level=log_level
        )
        log.info("获取任务配置", config=self.config)
        sanic_app = Sanic(app_name)
        sanic_app.config.FALLBACK_ERROR_FORMAT = "json"
        # 注册蓝图
        sanic_app.blueprint(api)
        # 注册listeners
        init_listeners(sanic_app)
        # 注册中间件
        init_middleware(sanic_app)
        # 启动
        host, port = self.config["address"].split(":")
        conf = {
            "host": host,
            "port": int(port),
            "workers": self.config.get("worker", 1),
            "debug": self.config.get("debug", True),
            "access_log": self.config.get("access_log", True),
        }
        if self.config.get("server_cert_path") and self.config.get("server_key_path"):
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.load_cert_chain(self.config.get("server_cert_path"), keyfile=self.config.get("server_key_path"))
            if self.config.get("ca_cert_path"):
                context.load_verify_locations(self.config.get("ca_cert_path"))
                context.verify_mode = ssl.CERT_REQUIRED
                if self.config.get('client_crl_path'):
                    context.load_verify_locations(self.config.get('client_crl_path'))
                    context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
                log.info("use TLS with client auth")
            else:
                log.info("use TLS")
            conf["ssl"] = context
        sanic_app.run(**conf)
