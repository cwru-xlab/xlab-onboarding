import functools
from typing import AnyStr, TypeVar

import bcrypt
import redis_om

T = TypeVar("T", bound=redis_om.RedisModel)


def migrate(model: T) -> T:
    @functools.wraps(model)
    def migrated():
        redis_om.Migrator().run()
        return model

    return migrated()


def hash_pwd(pwd: AnyStr, rounds: int = 12) -> bytes:
    return bcrypt.hashpw(_encode(pwd), bcrypt.gensalt(rounds))


def check_pwd(pwd: AnyStr, hashed: bytes) -> bool:
    return bcrypt.checkpw(_encode(pwd), hashed)


def _encode(s: AnyStr) -> bytes:
    return s if isinstance(s, bytes) else s.encode("utf-8")
