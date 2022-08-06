from __future__ import annotations

import functools
import warnings
from typing import Any, Optional, Type, TypeVar, Union, cast

import flask
import flask_security
import redis_om
from flask_security import datastore, forms
from pydantic import StrictBool, StrictStr, conlist
from redis_om import Field

T = TypeVar("T", bound=redis_om.RedisModel)
Permissions = Optional[
    Union[str, set[StrictStr], conlist(StrictStr, unique_items=True)]]


def migrate(model: T) -> T:
    @functools.wraps(model)
    def migrated():
        redis_om.Migrator().run()
        return model

    return migrated()


@migrate
class RedisRole(redis_om.JsonModel, flask_security.RoleMixin):
    name: StrictStr = Field(index=True)
    permissions: Permissions = set()


@migrate
class RedisUser(redis_om.JsonModel, flask_security.UserMixin):
    fs_uniquifier: StrictStr = Field(index=True)
    username: StrictStr = Field(index=True)
    password: StrictStr
    active: StrictBool = True
    roles: conlist(RedisRole, unique_items=True) = []

    def get_security_payload(self) -> dict[str, Any]:
        return self.dict()


Model = TypeVar("Model", bound=Union[RedisUser, RedisRole])


class RedisDatastore(datastore.Datastore):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(None)

    def put(self, model: Model) -> Model:
        return cast(Model, model.save())

    def delete(self, model: Model) -> None:
        Model.delete(model.pk)


class RedisUserDatastore(flask_security.UserDatastore, RedisDatastore):
    __slots__ = ()

    _supported = {"username", "fs_uniquifier"}

    def __init__(
            self,
            user: Type[RedisUser] = RedisUser,
            role: Type[RedisUser] = RedisRole
    ) -> None:
        super().__init__(user_model=user, role_model=role)

    def find_user(self, **kwargs) -> Optional[RedisUser]:
        if kwargs.pop("case_insensitive", False):
            warnings.warn("Redis does not support case-insensitive queries")
        result = None
        if attrs := self._query_by(set(kwargs)):
            query = (
                eval(f"{RedisUser.__name__}.{a}") == kwargs[a] for a in attrs)
            result = self._first_or_none(RedisUser.find(*query).all())
        return result

    def _query_by(self, requested: set[str]) -> set[str]:
        query_by = requested & self._supported
        if invalid := requested - self._supported:
            warnings.warn(
                f"Invalid query attributes {invalid}; querying by {query_by}")
        return query_by

    def find_role(self, role: str) -> Optional[RedisRole]:
        return self._first_or_none(RedisRole.find(RedisRole.name == role).all())

    @staticmethod
    def _first_or_none(result: list[Model]) -> Optional[Model]:
        return result[0] if result else None


class UsernameRegisterForm(flask_security.RegisterForm):
    """Hack to utilize RegisterForm, but use username instead of email."""

    email = forms.EmailField()  # Default: no validation


def init_app() -> flask_security.Security:
    flask.g.users = RedisUserDatastore()
    return flask_security.Security(
        flask.current_app, flask.g.users, register_form=UsernameRegisterForm)
