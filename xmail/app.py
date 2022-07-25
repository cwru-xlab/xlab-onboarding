from __future__ import annotations

from flask import Flask, current_app, g


def make_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.teardown_appcontext(_teardown_appcontext)
    with app.app_context():
        _ensure_instance_folder_exists()
        _set_hat_client()
        _add_routes()
    return app


def _ensure_instance_folder_exists() -> None:
    import os
    try:
        os.makedirs(current_app.instance_path)
    except OSError:
        pass


def _set_hat_client() -> None:
    if "hat_client" not in g:
        from hat import HatClient, ApiOwnerToken
        from settings import config
        g.hat_client = HatClient(ApiOwnerToken(config.hat_credential))


def _add_routes() -> None:
    import routes
    routes.add_routes()


def _teardown_appcontext(exception: BaseException) -> None:
    hat_client = g.pop("hat_client", None)
    if hat_client is not None:
        hat_client.close()