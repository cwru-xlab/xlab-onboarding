from typing import Any

import flask
import hat
import pydantic
from flask import Flask
from keyring.credentials import Credential
from pydantic import DirectoryPath, StrictStr


def init_app(app: Flask) -> None:
    config = Settings()
    app.config.from_object(config)
    flask.g.hat_client = config.hat_client()


class Settings(pydantic.BaseSettings):
    # Lowercase attributes: internal usage
    hat_username: StrictStr
    hat_password: StrictStr
    hat_namespace: StrictStr
    # Uppercase attributes: export directly
    FLASK_DEBUG: bool
    ASSETS_ROOT: DirectoryPath
    SECRET_KEY: StrictStr
    SECURITY_PASSWORD_SALT: StrictStr
    EMAIL_DOMAIN: StrictStr
    SECURITY_EMAIL_VALIDATOR_ARGS: dict[str, Any]

    class Config(pydantic.BaseSettings.Config):
        case_sensitive = False
        allow_mutation = False

    def hat_client(self) -> hat.HatClient:
        token = hat.ApiOwnerToken(self.hat_credential())
        return hat.HatClient(token)

    def hat_credential(self) -> Credential:
        class HatCredential(Credential):
            __slots__ = "_settings"

            def __init__(self, settings: Settings):
                self._settings = settings

            @property
            def username(self) -> str:
                return self._settings.hat_username

            @property
            def password(self) -> str:
                return self._settings.hat_password

        return HatCredential(self)
