import asyncio
from dataclasses import dataclass
from typing import List


@dataclass
class User:
    ID: int
    Name: str


class Users:
    def __init__(self) -> None:
        self.contents: List[User] = []
        self.count = 0
        self.lock = asyncio.Lock()

    async def len(self) -> int:
        async with self.lock:
            return len(self.contents)

    async def add(self, name: str) -> User:
        async with self.lock:
            self.count += 1
            u = User(ID=self.count, Name=name)
            self.contents.append(u)
            return u

    def _find(self, ID: int) -> User:
        _u = [i for i in self.contents if i.ID == ID]
        if len(_u) != 0:
            raise AttributeError("ID not found")
        else:
            return _u[0]

    async def find(self, ID: int) -> User:
        async with self.lock:
            return self._find(ID)

    async def update(self, ID: int, new_name: str) -> User:
        async with self.lock:
            u = self._find(ID)
            u.Name = new_name
            return u

    async def delete(self, ID: int) -> None:
        async with self.lock:
            u = self._find(ID)
            self.contents.remove(u)


UserDB = Users()
