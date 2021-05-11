import sys
from typing import List, Callable, Any, Dict
from pyloggerhelper import log
from schema_entry import EntryPoint



class App(EntryPoint):
    """jsonrpc项目的服务端启动入口."""
    _name = "{{ app_name }}"
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
                "default": "{{ app_name }}"
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
                
            },
            "access_log":{

            },
            "workers":{

            },
            "server_cert":{

            },
            "server_key":{

            },
            "authclient":
        }
    }
    register_instances: List[object]
    register_functions: Dict[str, Callable]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.register_instances = []
        self.register_functions = {}

    def register_instance(self, instance: object) -> None:
        self.register_instances.append(instance)

    def register_function(self, name: str, func: Callable) -> None:
        self.register_functions[name] = func

    def run(self) -> None:
        host, port = self.config["address"].split(":")
        nofif_pool.start()
        request_pool.start()
        with PooledJSONRPCServer((host, int(port)), thread_pool=request_pool) as server:
            # 注册所有可调用函数的名字到system.listMethods方法
            # 注册可调用函数的docstring到system.methodHelp(func_name)方法
            # 注册可调用函数的签名到system.methodSignature(func_name)方法
            server.set_notification_pool(nofif_pool)
            server.register_introspection_functions()
            # 这个函数的作用是可以使客户端同时调用服务端的的多个函数。
            server.register_multicall_functions()
            # 注册一个类的实例,使其中的成员方法作为可调用的函数
            for ins in self.register_instances:
                server.register_instance(ins)

            # 注册一个函数,使它可以被调用,后面的字符串就是被调用的函数名
            for name, func in self.register_functions.items():
                server.register_function(func, name)
            # Run the server's main loop
            log.info("jsonrpc start", address=f"tcp://{host}:{port}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                log.info("jsonrpc stoped!", address=f"tcp://{host}:{port}")
            except Exception as e:
                log.error("jsonrpc servic get error!", address=f"tcp://{host}:{port}", err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
                sys.exit(1)
            finally:
                request_pool.stop()
                nofif_pool.stop()
                server.set_notification_pool(None)
                log.info("jsonrpc stoped!", address=f"tcp://{host}:{port}")

    def do_main(self) -> None:
        log.initialize_for_app(
            app_name=self.config.get("app_name"),
            log_level=self.config.get("log_level")
        )
        log.info("获取任务配置", config=self.config)
        self.run()