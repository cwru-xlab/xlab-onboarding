from __future__ import annotations

import functools
import warnings
from typing import Any, Optional, Type, TypeVar, Union, cast

import flask
import flask_security as fs
from pydantic import StrictBool, StrictStr, conlist
from redis_om import Field, FindQuery, JsonModel, Migrator, NotFoundError, RedisModel

import forms

T = TypeVar("T", bound=RedisModel)
Permissions = Optional[Union[str, set[str], conlist(str, unique_items=True)]]


def migrate(model: T) -> T:
    @functools.wraps(model)
    def migrated():
        Migrator().run()
        return model

    return migrated()


@migrate
class RedisRole(JsonModel, fs.RoleMixin):
    name: StrictStr = Field(index=True)
    permissions: Permissions = set()


@migrate
class RedisUser(JsonModel, fs.UserMixin):
    fs_uniquifier: StrictStr = Field(index=True)
    username: StrictStr = Field(index=True)
    password: StrictStr
    active: StrictBool = True
    roles: conlist(RedisRole, unique_items=True) = []


Model = TypeVar("Model", bound=Union[RedisUser, RedisRole])


class RedisDatastore(fs.datastore.Datastore):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super(RedisDatastore, self).__init__(None)

    def put(self, model: Model) -> Model:
        return cast(Model, model.save())

    def delete(self, model: Model) -> None:
        model.delete(model.pk)


class RedisUserDatastore(fs.UserDatastore, RedisDatastore):
    __slots__ = ()

    _supported = {"username", "fs_uniquifier"}

    def __init__(
            self,
            user_model: Type[RedisUser] = RedisUser,
            role_model: Type[RedisRole] = RedisRole
    ) -> None:
        super().__init__(user_model, role_model)

    def find_user(self, **kwargs: Any) -> RedisUser | None:
        if kwargs.pop("case_insensitive", False):
            warnings.warn("Redis does not support case-insensitive queries")
        if attrs := self._query_by(set(kwargs)):
            query = (eval(f"{RedisUser.__name__}.{a}") == kwargs[a] for a in attrs)
            return self._first_or_none(RedisUser.find(*query))

    def _query_by(self, requested: set[str]) -> set[str]:
        query_by = requested & self._supported
        if invalid := requested - self._supported:
            warnings.warn(f"Invalid query attributes {invalid}; querying by {query_by}")
        return query_by

    def find_role(self, role: str) -> RedisRole | None:
        return self._first_or_none(RedisRole.find(RedisRole.name == role))

    @staticmethod
    def _first_or_none(result: FindQuery) -> Model | None:
        try:
            return result.first()
        except NotFoundError:
            return None


def init_app() -> fs.Security:
    security = fs.Security(register_form=forms.UsernameRegisterForm)
    security.init_app(flask.current_app, RedisUserDatastore())
    return security
