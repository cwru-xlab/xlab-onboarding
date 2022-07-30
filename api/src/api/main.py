from __future__ import annotations

from typing import Optional

import boto3
import fastapi
from aredis_om import model
from aws_error_utils import errors
from fastapi import responses, status
from pydantic import EmailStr, constr

import settings
import util

api = fastapi.FastAPI(default_response_class=responses.ORJSONResponse)
ses = boto3.resource("sesv2")


@util.migrate
class User(model.HashModel):
    username: constr(regex=r"[\w\-.]+", strict=True) = model.Field(index=True)
    recovery_email: EmailStr

    @classmethod
    async def lookup(cls, username: str) -> Optional[User]:
        match = await User.find(User.username == username).all()
        return None if not match else match[0]


@api.get("/users/{username}", status_code=status.HTTP_200_OK)
async def get_user(username: str) -> Optional[User]:
    if not (user := await User.lookup(username)):
        raise_user_not_found(username)
    return user


@api.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User) -> None:
    if not User.lookup(user.username):
        await User.save(user)
    else:
        raise_user_exists(user.username)


@api.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str) -> None:
    if user := await User.lookup(username):
        await User.delete(user.pk)
    else:
        raise_user_not_found(username)


def raise_user_not_found(username: str) -> None:
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User '{username}' not found")


def raise_user_exists(username: str) -> None:
    raise fastapi.HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User '{username}' already exists")


@api.post("/emails/", status_code=status.HTTP_201_CREATED)
def create_email(username: str) -> str:
    address = f"{username}@{settings.config.domain}"
    try:
        ses.create_email_identity(address)
        waiter = ses.get_waiter("identity_exists")
        waiter.wait(
            Identities=[address],
            WaiterConfig={"Delay": 3, "MaxAttempts": 20})
        return address
    except (errors.AlreadyExistsException,
            errors.LimitExceededException,
            errors.TooManyRequestsException,
            errors.BadRequestException,
            errors.ConcurrentModificationException,
            errors.NotFoundException) as e:
        raise fastapi.HTTPException(
            status_code=e.http_status_code, detail=e.message)
