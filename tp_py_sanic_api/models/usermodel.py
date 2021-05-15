"""用户自定义的orm映射.

注意使用装饰器register将要创建的表注册到Tables.
"""
from typing import Dict, Union
from pyloggerhelper import log
from tortoise.models import Model
from tortoise.fields import IntField, CharField, DatetimeField


class User(Model):
    id = IntField(pk=True)
    name = CharField(50)

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "name": self.name,
        }

    @classmethod
    async def init_Table(clz) -> None:
        usercount = await clz.all().count()
        if usercount == 0:
            await clz.create(name="admin")
            log.info("table user is empty, insert admin")
        else:
            log.info("table user is not empty")


__all__ = ["User"]
