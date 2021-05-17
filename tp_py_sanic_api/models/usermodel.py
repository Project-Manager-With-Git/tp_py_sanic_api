"""用户自定义的orm映射."""
from typing import Dict, Union
from pyloggerhelper import log
from tortoise.models import Model
from tortoise.fields import IntField, CharField, DatetimeField


class User(Model):
    id = IntField(pk=True)
    name = CharField(50)

    def __str__(self) -> str:
        return f"User {self.id}: {self.name}"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "name": self.name,
        }

    @classmethod
    async def init_Table(clz) -> None:
        log.info("init table user")
        usercount = await clz.all().count()
        if usercount == 0:
            await clz.create(name="admin")
            log.info("table user is empty, insert admin")
        else:
            log.info(f"table user is not empty,count {usercount}")


__all__ = ["User"]
