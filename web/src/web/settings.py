import flask
import hat
import pydantic
from flask import Flask
from keyring.credentials import Credential
from pydantic import DirectoryPath, StrictStr


def init_app(app: Flask) -> None:
    config = Settings()
    flask.g.hat_client = config.hat_client
    app.config["ASSETS_ROOT"] = config.assets_root
    app.config["SECRET_KEY"] = config.secret_key
    app.config["SECURITY_PASSWORD_SALT"] = config.security_password_salt
    app.config["EMAIL_DOMAIN"] = config.email_domain


class Settings(pydantic.BaseSettings):
    hat_username: StrictStr
    hat_password: StrictStr
    hat_namespace: StrictStr
    assets_root: DirectoryPath
    secret_key: StrictStr
    security_password_salt: StrictStr
    email_domain: StrictStr

    class Config:
        allow_mutation = False

    @property
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
