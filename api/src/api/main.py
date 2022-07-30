from __future__ import annotations

from typing import Optional

import fastapi
from pydantic import constr
from redis_om.model import model

from util import migrate

api = fastapi.FastAPI()


@migrate
class User(model.HashModel):
    username: constr(regex=r"[\w\-.]+", strict=True) = model.Field(index=True)

    @classmethod
    def create(cls, username: str, save: bool = True, **kwargs) -> User:
        if not (user := cls.lookup(username)):
            user = User(username=username, **kwargs)
            if save:
                user.save()
        return user

    @classmethod
    def destroy(cls, username: str) -> None:
        if user := cls.lookup(username):
            User.delete(user.pk)

    @classmethod
    def lookup(cls, username: str) -> Optional[User]:
        match = User.find(User.username == username).all()
        return None if not match else match[0]


@api.get("/")
def read_root():
    return {"Hello": "World"}


@api.get("/user/{username}")
def test_redis(username: str):
    return User.create(username)

# ses = boto3.resource("sesv2")


# class User(model.HashModel):
#     username: StrictStr = model.Field(index=True, regex=r"[\w\-\.]+")
#     recovery_email: EmailStr

# def add_new_user(username: str, recovery_email: str) -> None:
#     if User.find(User.username == username).all():
#         raise ValueError("Username already exists")
#     else:
#         User(username=username, recovery_email=recovery_email).save()


# def request_new_email(username: str) -> str:
#     # https://boto3.amazonaws.com/v1/documentation/api/latest/reference
#     # /services/sesv2.html#SESV2.Client.create_email_identity
#     try:
#         address = f"{username}@{settings.config.domain}"
#         response = ses.create_email_identity(address)
#     except exceptions.ClientError:
#         pass
