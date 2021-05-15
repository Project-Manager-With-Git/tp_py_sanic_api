import asyncio
import unittest
from pathlib import Path
from typing import Dict, Any
from aiounittest import async_test
from tp_py_sanic_api.app import new_app

from .defaultsanicconf import DefaultSanicConf


class APIQueryTest(unittest.TestCase):

    def setUp(self) -> None:
        app = new_app(DefaultSanicConf)
        self.cli = app.asgi_client
        print("section start with setuped aioclient for test context")

    def tearDown(self) -> None:
        print("section end")

    @async_test
    async def test_userlist_get(self) -> None:
        await asyncio.sleep(1)
        _, response = await self.cli.get("/v1/api/user")
        assert response.status == 200
        assert response.json.get("UserCount") == 0

    @async_test
    async def test_create_user(self) -> None:
        _, response = await self.cli.post("/v1/api/user", json={"name": "hsz"})
        assert response.status == 200
        assert response.json.get("uid") == 1

    @async_test
    async def test_get_user_info(self) -> None:
        _, response = await self.cli.post("/v1/api/user", json={"name": "hsz"})
        assert response.status == 200
        assert response.json.get("uid") == 1
        _, response = await self.cli.get("/v1/api/user/1")
        assert response.status == 200
        assert response.json.get("Name") == "hsz"

    @async_test
    async def test_update_user(self) -> None:
        _, response = await self.cli.post("/v1/api/user", json={"name": "hsz"})
        assert response.status == 200
        assert response.json.get("uid") == 1
        _, response = await self.cli.get("/v1/api/user/1")
        assert response.status == 200
        assert response.json.get("msg") == "更新成功"
        _, response = await self.cli.put("/v1/api/user/1", json={"name": "hsz1"})
        assert response.status == 200
        assert response.json.get("Name") == "hsz"
        _, response = await self.cli.get("/v1/api/user/1")
        assert response.status == 200
        assert response.json.get("Name") == "hsz1"
