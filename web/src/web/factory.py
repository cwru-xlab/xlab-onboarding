import os

import flask
import jinja2
from hat import HatClient

import settings


def make_app() -> flask.Flask:
    app = flask.Flask(__name__, instance_relative_config=True)
    app.teardown_appcontext(_teardown_appcontext)
    with app.app_context():
        settings.init_app(app)
        _ensure_instance_folder_exists()

    @app.route("/", defaults={"path": "index.html"})
    @app.route("/<path:path>")
    def index(path: str):
        try:
            current_page = flask.request.path.split("/")[-1] or "index"
            return flask.render_template("home/" + path, segment=current_page)
        except jinja2.TemplateNotFound:
            return flask.render_template("home/page-404.html"), 404

    return app


def _teardown_appcontext(exception: BaseException) -> None:
    hat_client: HatClient = flask.g.pop("hat_client", None)
    if hat_client is not None:
        hat_client.close()


def _ensure_instance_folder_exists() -> None:
    try:
        os.makedirs(flask.current_app.instance_path)
    except OSError:
        pass
