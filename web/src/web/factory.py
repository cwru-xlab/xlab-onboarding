from __future__ import annotations

import itertools
import os.path
import sys
from typing import Any, Callable, Iterable, cast

import flask
import flask_security as fs
from flask.typing import ErrorHandlerCallable
from hat import HatClient
from pydantic import EmailStr

import auth
import settings
from auth import RedisUserDatastore
from forms import EmailsToDelete
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

    @app.route("/inbox", methods=["GET", "POST"])
    @fs.auth_required()
    def inbox() -> str | flask.Response:
        if get := flask.request.method == "GET":
            hat_client().clear_cache()
        emails = get_emails()
        form = create_form(emails)
        if not get and form.validate_on_submit():
            Email.delete_all(e for e in emails if e.uid in form.emails.data)
            result = app.redirect(flask.url_for("inbox"))
        else:
            # This must be a collection to iterate over it multiple times.
            emails = list(zip(emails, form.emails))
            result = render_template("inbox.html", emails=emails, form=form)
        return result

    @app.route("/send/<to>")
    @fs.auth_required()
    def send(to: str):
        email = Email(
            headers=EmailHeaders(
                to=f"{to}@xmail.com",
                sender=f"{current_user()}@xmail.com",
                subject="Hello world!"),
            body="Can you hear me?")
        if sent := send_email(email):
            return sent.dict()
        else:
            return "Email not sent", 200

    @app.route("/received")
    @fs.auth_required()
    def received():
        hat_client().clear_cache()
        return [e.dict() for e in Email.get(current_user())]

    @app.route("/clear")
    @fs.auth_required()
    def clear():
        client = Email.client
        return client.delete(*client.get(current_user()))

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


def get_emails() -> list[Email]:
    # Emails should be returned in a consistent order to delete them.
    emails = Email.get(current_user())
    return sorted(emails, key=lambda e: e.headers.date, reverse=True)


def create_form(emails: list[Email]) -> EmailsToDelete:
    form = EmailsToDelete()
    form.emails.choices = [e.uid for e in emails]
    return form


def current_user() -> str:
    return fs.current_user.username


def hat_client() -> HatClient:
    return flask.current_app.config.HAT_CLIENT


def teardown_appcontext(exception: BaseException | None) -> None:
    hat_client().close()


def error_handler(code: int) -> ErrorHandlerCallable:
    return lambda e: (render_template(f"{code}.html"), code)


def render_template(path: str, **context) -> str:
    path = os.path.join(flask.current_app.config.PAGES_DIR, path)
    return flask.render_template(path, **context)


def split(iterable: Iterable, pred: Callable[[Any], bool]) -> tuple[list, list]:
    iterable = list(iterable)
    true = list(filter(pred, iterable))
    false = list(itertools.filterfalse(pred, iterable))
    return true, false
