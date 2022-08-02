from __future__ import annotations

from typing import Optional

import pydantic
from aredis_om import model
from pydantic import conbytes, constr

import util

Username = constr(regex=r"[\w\-.]+", strict=True)


class PlainUser(pydantic.BaseModel):
    username: Username
    pwd: constr(strip_whitespace=True, strict=True)

    class Config:
        allow_mutation = False


@util.migrate
class ExistingUser(model.HashModel):
    username: Username = model.Field(index=True)
    pwd_hash: conbytes(strip_whitespace=True, strict=True)

    @classmethod
    async def lookup(cls, username: str) -> Optional[ExistingUser]:
        match = await cls.find(cls.username == username).all()
        return None if not match else match[0]

    @classmethod
    async def check_password(cls, user: PlainUser) -> bool:
        result = False
        if existing := await cls.lookup(user.username):
            result = util.check_pwd(user.pwd, existing.pwd_hash)
        return result

    @classmethod
    async def create(cls, user: PlainUser) -> None:
        hashed = util.hash_pwd(user.pwd)
        await ExistingUser(username=user.username, pwd_hash=hashed).save()
