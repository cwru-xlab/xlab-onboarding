import functools
from typing import TypeVar

import redis_om

T = TypeVar("T", bound=redis_om.RedisModel)


def migrate(model: T) -> T:
    @functools.wraps(model)
    def migrated():
        redis_om.Migrator().run()
        return model

    return migrated()
