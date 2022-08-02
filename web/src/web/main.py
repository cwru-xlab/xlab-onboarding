# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import flask
import jinja2

import settings

app = flask.Flask(__name__)
settings.init_app(app)


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def index(path: str):
    try:
        current_page = flask.request.path.split("/")[-1] or "index"
        return flask.render_template("home/" + path, segment=current_page)
    except jinja2.TemplateNotFound:
        return flask.render_template("home/page-404.html"), 404
