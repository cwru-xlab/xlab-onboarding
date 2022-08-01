from __future__ import annotations

from typing import Optional

import fastapi
from aredis_om import model
from fastapi import responses, status
from pydantic import constr

import settings
import util

USER_TAG = ["user"]
EMAIL_TAG = ["email"]

config = settings.Settings()
api = fastapi.FastAPI(default_response_class=responses.ORJSONResponse)


@util.migrate
class User(model.HashModel):
    username: constr(regex=r"[\w\-.]+", strict=True) = model.Field(index=True)

    @classmethod
    async def lookup(cls, username: str) -> Optional[User]:
        match = await User.find(User.username == username).all()
        return None if not match else match[0]


@api.get("/users/{username}", status_code=status.HTTP_200_OK, tags=USER_TAG)
async def get_user(username: str) -> Optional[User]:
    if not (user := await User.lookup(username)):
        raise_user_not_found(username)
    return user


@api.post("/users/", status_code=status.HTTP_201_CREATED, tags=USER_TAG)
async def create_user(user: User) -> None:
    if not User.lookup(user.username):
        await User.save(user)
    else:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User '{user.username}' already exists")


@api.delete(
    "/users/{username}", status_code=status.HTTP_204_NO_CONTENT, tags=USER_TAG)
async def delete_user(username: str) -> None:
    if user := await User.lookup(username):
        await User.delete(user.pk)
    else:
        raise_user_not_found(username)


def raise_user_not_found(username: str) -> None:
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User '{username}' not found")
