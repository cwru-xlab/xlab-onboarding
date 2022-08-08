from __future__ import annotations

import os.path

import flask
import flask_security
from flask.typing import ErrorHandlerCallable
from hat import HatClient
from pydantic import NameEmail

import auth
import settings
from auth import RedisUserDatastore
from models import Email
from settings import AttrConfig


def make_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.teardown_appcontext(teardown_appcontext)
    with app.app_context():
        settings.init_app()  # Run early on to load configuration.
        security = auth.init_app()
        for code in (403, 404, 500):
            app.register_error_handler(code, error_handler(code))

    @app.route("/")
    def root() -> flask.Response:
        # noinspection PyUnresolvedReferences
        return app.redirect(app.url_for("home"))

    @app.route("/home")
    def home() -> flask.Response:
        # noinspection PyUnresolvedReferences
        return app.redirect(security.login_url)

    @app.route("/inbox")
    @flask_security.auth_required()
    def inbox() -> str:
        return flask.render_template(format_path("tables.html"))

    def get_emails(username: str) -> list[Email]:
        return Email.get(username)

    def delete_email(email: Email) -> None:
        email.delete()

    def send_email(email: Email) -> None:
        email.save(check_to(email.headers.to))

    def check_to(to: NameEmail) -> str:
        username, domain = to.email.split("@")
        # Check that email domain is correct.
        config: AttrConfig = flask.current_app.config
        if domain != config.EMAIL_DOMAIN:
            raise ValueError(f"Email domain must be {config.EMAIL_DOMAIN}")
        # Check that the email address exists.
        users: RedisUserDatastore = flask.g.get("users")
        if not users.find_user(username=username):
            raise ValueError(f"{to.email} does not exist")
        return username

    return app


def teardown_appcontext(exception: BaseException | None) -> None:
    hat_client: HatClient = flask.g.pop("hat_client", None)
    if hat_client is not None:
        hat_client.close()


def error_handler(code: int) -> ErrorHandlerCallable:
    template = format_path(f"{code}.html")
    return lambda e: (flask.render_template(template), code)


def format_path(path: str) -> str:
    return os.path.join(flask.current_app.config.PAGES_DIR, path)
