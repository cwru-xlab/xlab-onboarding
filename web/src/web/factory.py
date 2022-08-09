from __future__ import annotations

import os.path
import pprint
import sys
from typing import cast

import flask
import flask_security as fs
from flask.typing import ErrorHandlerCallable
from hat import HatClient
from pydantic import EmailStr

import auth
import settings
from auth import RedisUserDatastore
from models import Email, EmailHeaders
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
    @fs.auth_required()
    def inbox() -> str:
        hat_client().clear_cache()
        return flask.render_template(format_path("tables.html"))

    @app.route("/send/<to>")
    @fs.auth_required()
    def send(to: str):
        email = Email(
            headers=EmailHeaders(
                to=f"{to}@xmail.com",
                sender=f"{current_user().username}@xmail.com",
                subject="Hello world!"),
            body="Can you hear me?")
        pprint.pp(email.dict(), indent=2, stream=sys.stderr)
        if sent := send_email(email):
            return sent.dict()
        else:
            return "Email not sent", 200

    @app.route("/received")
    @fs.auth_required()
    def received():
        hat_client().clear_cache()
        return [e.dict() for e in Email.get(current_user().username)]

    @app.route("/clear")
    @fs.auth_required()
    def clear():
        client = Email.client
        return client.delete(*client.get(current_user().username))

    def get_emails(username: str) -> list[Email]:
        return Email.get(username)

    def delete_email(email: Email) -> None:
        email.delete()

    def send_email(email: Email) -> Email:
        to, valid = check_to(email.headers.to)
        if valid:
            return email.save(to)

    def check_to(to: EmailStr) -> tuple[str, bool]:
        username, domain = to.split("@")
        # Check that email domain is correct.
        config: AttrConfig = flask.current_app.config
        valid = True
        if domain != config.EMAIL_DOMAIN:
            print(
                f"Email domain must be {config.EMAIL_DOMAIN}; got {domain}",
                file=sys.stderr)
            valid = False
        # Check that the email address exists.
        users = cast(RedisUserDatastore, security.datastore)
        if not users.find_user(username=username):
            print(f"{to} does not exist", file=sys.stderr)
            valid = False
        return username, valid

    return app


def current_user() -> auth.RedisUser:
    return fs.current_user


def hat_client() -> HatClient:
    return flask.current_app.config.HAT_CLIENT


def teardown_appcontext(exception: BaseException | None) -> None:
    hat_client().close()


def error_handler(code: int) -> ErrorHandlerCallable:
    template = format_path(f"{code}.html")
    return lambda e: (flask.render_template(template), code)


def format_path(path: str) -> str:
    return os.path.join(flask.current_app.config.PAGES_DIR, path)
