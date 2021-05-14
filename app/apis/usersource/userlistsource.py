from sanic.response import json, HTTPResponse
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_openapi import openapi
from decorators.checkjsonschema import checkjsonschema
from modules.usermodule import UserDB


post_query_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": False,
    "required": ["name"],
    "properties": {
        "name": {
            "type": "string",
            "description": "用户注册名"
        }
    }
}


class UserListSource(HTTPMethodView):
    async def get(self, _: Request) -> HTTPResponse:
        cnt = await UserDB.len()
        result = {
            "description": "测试api,User总览",
            "user-count": cnt,
            "links": [
                {
                    "uri": "/user",
                    "method": "POST",
                    "description": "创建一个新用户"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "GET",
                    "description": "用户号为<id>的用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "PUT",
                    "description": "更新用户号为<id>用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "DELETE",
                    "description": "删除用户号为<id>用户"
                },
            ]
        }

        return json(result, ensure_ascii=False)

    @checkjsonschema(post_query_schema)
    async def post(self, request: Request) -> HTTPResponse:
        query_json = request.json
        try:
            u = await UserDB.add(query_json.get("name", ""))
        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            return json({
                "msg": "插入成功",
                "uid": u.ID
            }, ensure_ascii=False)
