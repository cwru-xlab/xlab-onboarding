from typing import Any, Callable, Optional

import flask
import flask_security as fs
import pydantic
from hat import client
from keyring import credentials
from pydantic import DirectoryPath, conlist

IdAttr = dict[str, dict[str, Any]]
Mapper = Callable[[str], Optional[str]]


def init_app() -> None:
    app = flask.current_app
    config = AttrConfig(app.config.root_path)
    config.update(app.config)
    settings = Settings()
    config.from_object(settings)
    app.config = config
    client.set_client(settings.hat_client)


def id_attr(attr: str, *, mapper: Mapper, case_insensitive: bool) -> IdAttr:
    return {attr: {"mapper": mapper, "case_insensitive": case_insensitive}}


# noinspection PyPep8Naming
class Settings(pydantic.BaseSettings):
    # HAT SDK
    hat_username: str
    hat_password: str
    hat_namespace: str
    # Flask
    FLASK_DEBUG: bool = True
    # Flask-Security: Core
    SECRET_KEY: str
    SECURITY_PASSWORD_SALT: str
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: Optional[str] = "zxcvbn"
    SECURITY_PASSWORD_CHECK_BREACHED: Optional[str] = "best-effort"
    SECURITY_REDIRECT_VALIDATE_MODE: str = "regex"
    SECURITY_CSRF_COOKIE: dict[str, Any] = {
        # Overrides default secure = False to require HTTPS.
        "samesite": "Strict", "httponly": False, "secure": True}
    SECURITY_USER_IDENTITY_ATTRIBUTES: conlist(IdAttr) = [
        id_attr("username", mapper=fs.uia_username_mapper, case_insensitive=False)]
    # Flask-Security: Core – rarely need changing
    SECURITY_LOGIN_SALT: str
    # Flask-Security: Login/logout
    SECURITY_POST_LOGIN_VIEW: str = "/inbox"
    # Flask-Security: Registerable
    SECURITY_REGISTERABLE: bool = True
    SECURITY_SEND_REGISTER_EMAIL: bool = False
    SECURITY_USERNAME_ENABLE: bool = True
    SECURITY_USERNAME_REQUIRED: bool = True
    # Flask-Security: Messages
    SECURITY_MSG_USERNAME_INVALID_LENGTH: tuple[str, str] = (
        "Username must be %(min)d – %(max)d characters", "error")
    # xMail
    ASSETS_ROOT: DirectoryPath = "./static/assets"  # Relative to the app root
    EMAIL_DOMAIN: str = "xmail.com"
    PAGES_DIR: str = "home"  # Relative to "templates" dir. Do NOT include "./"

    # Flask-Security: Login/logout (cont.)
    @property
    def SECURITY_LOGIN_USER_TEMPLATE(self) -> str:
        return f"{self.PAGES_DIR}/page-sign-in.html"

    # Flask-Security: Registerable (cont.)
    @property
    def SECURITY_REGISTER_USER_TEMPLATE(self) -> str:
        return f"{self.PAGES_DIR}/page-sign-up.html"

    @property
    def hat_client(self) -> client.HatClient:
        http_client = client.HttpClient()
        credential = credentials.SimpleCredential(self.hat_username, self.hat_password)
        token = client.CredentialOwnerToken(http_client, credential)
        return client.HatClient(http_client, token, self.hat_namespace)


class AttrConfig(flask.Config):
    # Source: https://github.com/pallets/flask/issues/1992#issue-172434213

    def __init__(self, root_path: str, **kwargs) -> None:
        super().__init__(root_path, **kwargs)

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key.upper()]
        except KeyError:
            raise AttributeError(f"Invalid config option: {key}")

    def __setattr__(self, key: str, value: Any) -> None:
        self[key.upper()] = value
