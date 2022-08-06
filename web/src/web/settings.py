from pathlib import Path
from typing import Any

import flask
import hat
import pydantic
from keyring.credentials import Credential
from pydantic import DirectoryPath


def init_app() -> None:
    app = flask.current_app
    config = AttrConfig(app.config.root_path)
    config.update(app.config)
    config.from_object(s := Settings())
    app.config = config
    hat.ActiveHatModel.client = flask.g.hat_client = s.hat_client()


class Settings(pydantic.BaseSettings):
    # Lowercase attributes: internal usage
    hat_username: str
    hat_password: str
    hat_namespace: str
    # Uppercase attributes: export directly
    FLASK_DEBUG: bool
    PAGES_DIR: Path
    ASSETS_ROOT: DirectoryPath
    EMAIL_DOMAIN: str

    SECRET_KEY: str
    SECURITY_LOGIN_SALT: str
    SECURITY_PASSWORD_SALT: str
    SECURITY_PASSWORD_HASH: str
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: str
    SECURITY_PASSWORD_CHECK_BREACHED: str
    SECURITY_EMAIL_VALIDATOR_ARGS: dict[str, Any]
    SECURITY_POST_LOGIN_VIEW: str
    SECURITY_UNAUTHORIZED_VIEW: str
    SECURITY_LOGIN_USER_TEMPLATE: str
    SECURITY_REGISTER_USER_TEMPLATE: str
    SECURITY_REGISTERABLE: bool
    SECURITY_SEND_REGISTER_EMAIL: bool
    SECURITY_USERNAME_ENABLE: bool
    SECURITY_USERNAME_REQUIRED: bool

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


class AttrConfig(flask.Config):
    # Source: https://github.com/pallets/flask/issues/1992#issue-172434213

    def __init__(self, root_path: str, **kwargs) -> None:
        super().__init__(root_path, **kwargs)

    def __getattr__(self, attr: str) -> Any:
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"Invalid config option: {attr}")
