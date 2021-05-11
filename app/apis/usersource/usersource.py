from dataclasses import asdict
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json, HTTPResponse
from jsonschema import validate
from decorators.checkjsonschema import checkjsonschema
from .usermodule import UserDB


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
    async def get(self, _: Request, uid: int) -> HTTPResponse:
        try:
            u = await UserDB.find(uid)
        except AttributeError:
            return json({
                "msg": "未找到用户",
            }, status=404, ensure_ascii=False)
        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            return json(asdict(u), ensure_ascii=False)

    @checkjsonschema(put_query_schema)
    async def put(self, request: Request, uid: int) -> HTTPResponse:
        query_json = request.json
        try:
            validate(instance=query_json, schema=put_query_schema)
        except Exception as e:
            return json({
                "msg": "参数错误",
                "error": str(e)
            }, status=401, ensure_ascii=False)
        else:
            try:
                await UserDB.update(uid, query_json.get("name", ""))
            except AttributeError:
                return json({
                    "msg": "未找到用户",
                }, status=404, ensure_ascii=False)
            except Exception as e:
                return json({
                    "msg": "执行错误",
                }, status=500, ensure_ascii=False)
            else:
                return json({"msg": "更新成功"}, ensure_ascii=False)
   
    async def delete(self, _: Request, uid: int) -> HTTPResponse:
        try:
            await UserDB.delete(uid)
        except AttributeError:
            return json({
                "msg": "未找到用户",
            }, status=404, ensure_ascii=False)
        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            return json({"msg": "删除成功"}, ensure_ascii=False)
