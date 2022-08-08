from typing import Any, Callable, Optional

import flask
import flask_security as fs
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


UserIdentityAttribute = dict[str, dict[str, Any]]
Mapper = Callable[[str], Optional[str]]


def user_id_attribute(
        attribute: str, mapper: Mapper, case_insensitive: bool
) -> UserIdentityAttribute:
    return {attribute: {
        "mapper": mapper,
        "case_insensitive": case_insensitive}}


# noinspection PyPep8Naming
class Settings(pydantic.BaseSettings):
    # Lowercase attributes are for internal-use only.
    # Flask only imports uppercase attributes.

    # Secrets
    hat_username: str
    hat_password: str
    hat_namespace: str
    SECRET_KEY: str
    SECURITY_LOGIN_SALT: str
    SECURITY_PASSWORD_SALT: str

    FLASK_DEBUG: bool = True
    ASSETS_ROOT: DirectoryPath = "./static/assets"  # Relative to the app root
    EMAIL_DOMAIN: str = "xmail.com"
    PAGES_DIR: str = "home"  # Relative to "templates" dir. Do NOT include "./"
    SECURITY_PASSWORD_HASH: str = "bcrypt"
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: Optional[str] = "zxcvbn"
    SECURITY_PASSWORD_CHECK_BREACHED: Optional[str] = "best-effort"
    SECURITY_POST_LOGIN_VIEW: str = "/inbox"
    SECURITY_REGISTERABLE: bool = True
    SECURITY_SEND_REGISTER_EMAIL: bool = False
    SECURITY_LOGIN_WITHOUT_CONFIRMATION: bool = True
    SECURITY_USERNAME_ENABLE: bool = True
    SECURITY_USERNAME_REQUIRED: bool = True
    SECURITY_USER_IDENTITY_ATTRIBUTES: list[UserIdentityAttribute] = [
        user_id_attribute(
            attribute="username",
            mapper=fs.uia_username_mapper,
            case_insensitive=False)]
    SECURITY_REDIRECT_VALIDATE_MODE: str = "regex"
    SECURITY_MSG_USERNAME_INVALID_LENGTH: tuple[str, str] = (
        "Username must be %(min)d – %(max)d characters", "error")

    class Config(pydantic.BaseSettings.Config):
        allow_mutation = False

    @property
    def SECURITY_LOGIN_USER_TEMPLATE(self) -> str:
        return f"{self.PAGES_DIR}/login.html"

    @property
    def SECURITY_REGISTER_USER_TEMPLATE(self) -> str:
        return f"{self.PAGES_DIR}/register.html"

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
