from typing import Any, Callable, Optional

import flask
import flask_security as fs
import pydantic
from hat import client
from keyring import credentials
from pydantic import DirectoryPath, StrictBool, StrictStr, conlist


def init_app() -> None:
    app = flask.current_app
    config = AttrConfig(app.config.root_path)
    config.update(app.config)
    config.from_object(Settings())
    app.config = config
    client.set_client(config.HAT_CLIENT)


IdAttr = dict[StrictStr, dict[StrictStr, Any]]
Mapper = Callable[[StrictStr], Optional[StrictStr]]


def id_attr(attr: str, *, mapper: Mapper, case_insensitive: bool) -> IdAttr:
    return {attr: {"mapper": mapper, "case_insensitive": case_insensitive}}


# noinspection PyPep8Naming
class Settings(pydantic.BaseSettings):
    # Lowercase attributes are for internal-use only.
    # Flask only imports uppercase attributes.

    # Secrets
    hat_username: StrictStr
    hat_password: StrictStr
    hat_namespace: StrictStr
    SECRET_KEY: StrictStr
    SECURITY_LOGIN_SALT: StrictStr
    SECURITY_PASSWORD_SALT: StrictStr

    FLASK_DEBUG: StrictBool = True
    ASSETS_ROOT: DirectoryPath = "./static/assets"  # Relative to the app root
    EMAIL_DOMAIN: StrictStr = "xmail.com"
    # Relative to "templates" dir. Do NOT include "./"
    PAGES_DIR: StrictStr = "home"
    SECURITY_PASSWORD_HASH: StrictStr = "bcrypt"
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: Optional[StrictStr] = "zxcvbn"
    SECURITY_PASSWORD_CHECK_BREACHED: Optional[StrictStr] = "best-effort"
    SECURITY_POST_LOGIN_VIEW: StrictStr = "/inbox"
    SECURITY_REGISTERABLE: StrictBool = True
    SECURITY_SEND_REGISTER_EMAIL: StrictBool = False
    SECURITY_LOGIN_WITHOUT_CONFIRMATION: StrictBool = True
    SECURITY_USERNAME_ENABLE: StrictBool = True
    SECURITY_USERNAME_REQUIRED: StrictBool = True
    SECURITY_USER_IDENTITY_ATTRIBUTES: conlist(IdAttr) = [
        id_attr("username", mapper=fs.uia_username_mapper, case_insensitive=False)]
    SECURITY_REDIRECT_VALIDATE_MODE: StrictStr = "regex"
    # Overrides default secure = False to require HTTPS.
    SECURITY_CSRF_COOKIE: dict[StrictStr, Any] = {
        "samesite": "Strict", "httponly": False, "secure": True}
    SECURITY_MSG_USERNAME_INVALID_LENGTH: tuple[StrictStr, StrictStr] = (
        "Username must be %(min)d – %(max)d characters", "error")

    @property
    def SECURITY_LOGIN_USER_TEMPLATE(self) -> str:
        return f"{self.PAGES_DIR}/login.html"

    @property
    def SECURITY_REGISTER_USER_TEMPLATE(self) -> str:
        return f"{self.PAGES_DIR}/register.html"

    @property
    def HAT_CLIENT(self) -> client.HatClient:
        http_client = client.HttpClient()
        credential = credentials.SimpleCredential(self.hat_username, self.hat_password)
        token = client.CredentialOwnerToken(http_client, credential)
        return client.HatClient(http_client, token, self.hat_namespace)


class AttrConfig(flask.Config):
    # Source: https://github.com/pallets/flask/issues/1992#issue-172434213

    def __init__(self, root_path: str, **kwargs) -> None:
        super().__init__(root_path, **kwargs)

    def __getattr__(self, attr: str) -> Any:
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"Invalid config option: {attr}")
