import functools
import os.path
from typing import Callable

import flask
import flask_security
import jinja2
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
        settings.init_app()
        auth.init_app()

    @app.route("/", defaults={"path": "index.html"})
    @app.route("/<path:path>")
    @with_fallback
    def index(path: str):
        return flask.render_template(
            format_path(path), segment=path.split("/")[-1] or "index")

    @app.route("/inbox")
    @flask_security.auth_required()
    @with_fallback
    def inbox():
        pass

    def get_emails(username: str) -> list[Email]:
        return Email.get(username)

    def delete_email(email: Email) -> None:
        email.delete()

    def send_email(email: Email) -> None:
        username = check_to(email.headers.to)
        email.save(username)

    def check_to(to: NameEmail) -> str:
        username, domain = to.email.split("@")
        # Check that email domain is correct.
        config: AttrConfig = flask.current_app.config
        if domain != (expected := config.EMAIL_DOMAIN):
            raise ValueError(f"Email address domains must be {expected}")
        # Check that the email address exists.
        users: RedisUserDatastore = flask.g.get("users")
        if not users.find_user(username=username):
            raise ValueError(f"Email address {to.email} does not exist")
        return username

    return app


def with_fallback(render) -> Callable[[...], str]:
    @functools.wraps(render)
    def wrapped(*args, **kwargs):
        try:
            return render(*args, **kwargs)
        except jinja2.TemplateNotFound:
            return flask.render_template(format_path("404.html")), 404

    return wrapped


def format_path(path: str) -> str:
    return os.path.join(flask.current_app.config.PAGES_DIR, path)


def teardown_appcontext(exception: BaseException) -> None:
    hat_client: HatClient = flask.g.pop("hat_client", None)
    if hat_client is not None:
        hat_client.close()
