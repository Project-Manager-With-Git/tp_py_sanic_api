from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic_openapi import doc
from ...decorators.checkjsonschema import checkjsonschema
from ...models import User


put_query_schema = {
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


class UserSource(HTTPMethodView):

    @doc.summary("获取用户信息")
    async def get(self, _: Request, uid: int) -> HTTPResponse:
        try:
            u = await User.get_or_none(id=uid)
        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            if u:
                return json(u.to_dict(), ensure_ascii=False)
            else:
                return json({
                    "msg": "未找到用户",
                }, status=404, ensure_ascii=False)

    @staticmethod
    @doc.summary("更新用户信息")
    @checkjsonschema(put_query_schema)
    async def put(request: Request, uid: int) -> HTTPResponse:
        query_json = request.json
        try:
            u = await User.get_or_none(id=uid)
            if not u:
                return json({
                    "msg": "未找到用户",
                }, status=404, ensure_ascii=False)
            else:
                u.name = query_json.get("name", "")
                await u.save(update_fields=["name"])
        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            return json({"msg": "更新成功"}, ensure_ascii=False)

    @doc.summary("删除用户")
    async def delete(self, _: Request, uid: int) -> HTTPResponse:
        try:
            u = await User.get_or_none(id=uid)
            if not u:
                return json({
                    "msg": "未找到用户",
                }, status=404, ensure_ascii=False)
            else:
                await u.delete()
        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            return json({"msg": "删除成功"}, ensure_ascii=False)
