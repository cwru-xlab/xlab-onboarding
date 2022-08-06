from __future__ import annotations

import functools
from typing import Any, Optional, Type, TypeVar, Union, cast

import flask
import flask_security
import redis_om
from flask_security import datastore
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

    VALID_USER_QUERY_ATTRIBUTES = {"email", "username", "fs_uniquifier"}

    def __init__(
            self,
            user: Type[RedisUser] = RedisUser,
            role: Type[RedisUser] = RedisRole
    ) -> None:
        super().__init__(user_model=user, role_model=role)

    def find_user(self, **kwargs) -> Optional[RedisUser]:
        result = None
        if valid := self.VALID_USER_QUERY_ATTRIBUTES.intersection(kwargs):
            query = (
                eval(f"{RedisUser.__name__}.{v}") == kwargs[v] for v in valid)
            result = RedisUser.find(*query).all()
            result = self._first_or_none(result)
        return result

    def find_role(self, role: str) -> Optional[RedisRole]:
        result = RedisRole.find(RedisRole.name == role).all()
        return self._first_or_none(result)

    @staticmethod
    def _first_or_none(result: list[Model]) -> Optional[Model]:
        return result[0] if result else None


def init_app() -> None:
    flask.g.users = RedisUserDatastore()
    flask_security.Security(flask.current_app, flask.g.users)
