from __future__ import annotations

import fastapi
from fastapi import responses, status

import models

USER_TAG = ["user"]
EMAIL_TAG = ["email"]

api = fastapi.FastAPI(default_response_class=responses.ORJSONResponse)


@api.get("/users/", status_code=status.HTTP_200_OK, tags=USER_TAG)
async def get_user(username: str) -> models.ExistingUser:
    if not (user := await models.ExistingUser.lookup(username)):
        raise_user_not_found(username)
    return user


@api.post("/users/check", status_code=status.HTTP_200_OK, tags=USER_TAG)
async def check_password(user: models.PlainUser) -> bool:
    return await models.ExistingUser.check_password(user)


@api.post("/users/create", status_code=status.HTTP_201_CREATED, tags=USER_TAG)
async def create_user(user: models.PlainUser) -> None:
    if not models.ExistingUser.lookup(user.username):
        await models.ExistingUser.create(user)
    else:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User '{user.username}' already exists")


@api.delete("/users/", status_code=status.HTTP_204_NO_CONTENT, tags=USER_TAG)
async def delete_user(username: str) -> None:
    if user := await models.ExistingUser.lookup(username):
        await models.ExistingUser.delete(user.pk)
    else:
        raise_user_not_found(username)


def raise_user_not_found(username: str) -> None:
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User '{username}' not found")
