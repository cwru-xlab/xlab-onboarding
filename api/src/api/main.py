from __future__ import annotations

from typing import Optional

import fastapi
import pydantic
from aredis_om import model
from fastapi import responses, status
from pydantic import conbytes, constr

import util

USER_TAG = ["user"]
EMAIL_TAG = ["email"]
Username = constr(regex=r"[\w\-.]+", strict=True)

api = fastapi.FastAPI(default_response_class=responses.ORJSONResponse)


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


@api.get("/users/", status_code=status.HTTP_200_OK, tags=USER_TAG)
async def get_user(username: str) -> ExistingUser:
    if not (user := await ExistingUser.lookup(username)):
        raise_user_not_found(username)
    return user


@api.post("/users/check", status_code=status.HTTP_200_OK, tags=USER_TAG)
async def check_password(user: PlainUser) -> bool:
    return await ExistingUser.check_password(user)


@api.post("/users/create", status_code=status.HTTP_201_CREATED, tags=USER_TAG)
async def create_user(user: PlainUser) -> None:
    if not ExistingUser.lookup(user.username):
        await ExistingUser.create(user)
    else:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User '{user.username}' already exists")


@api.delete("/users/", status_code=status.HTTP_204_NO_CONTENT, tags=USER_TAG)
async def delete_user(username: str) -> None:
    if user := await ExistingUser.lookup(username):
        await ExistingUser.delete(user.pk)
    else:
        raise_user_not_found(username)


def raise_user_not_found(username: str) -> None:
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User '{username}' not found")
