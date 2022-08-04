import functools
from typing import Callable

import flask
import flask_security
import jinja2
from hat import HatClient

import auth
import settings


def make_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.teardown_appcontext(teardown_appcontext)
    settings.init_app(app)
    auth.init_app(app)

    @app.route("/", defaults={"path": "index.html"})
    @app.route("/<path:path>")
    @with_fallback
    def index(path: str):
        current_page = flask.request.path.split("/")[-1] or "index"
        return flask.render_template("home/" + path, segment=current_page)

    @app.route("/inbox")
    @flask_security.auth_required()
    @with_fallback
    def inbox():
        pass

    return app


def with_fallback(render) -> Callable[[...], str]:
    @functools.wraps(render)
    def wrapped(*args, **kwargs):
        try:
            return render(*args, **kwargs)
        except jinja2.TemplateNotFound:
            return flask.render_template("home/404.html"), 404

    return wrapped


def teardown_appcontext(exception: BaseException) -> None:
    hat_client: HatClient = flask.g.pop("hat_client", None)
    if hat_client is not None:
        hat_client.close()
