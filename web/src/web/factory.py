from __future__ import annotations

import os
from typing import Iterable

import flask
import flask_security as fs
from flask import Response
from flask.typing import ErrorHandlerCallable
from hat import client
from pydantic import EmailStr

import auth
import forms
import models
import settings


def make_app() -> flask.Flask:
    app = flask.Flask(__name__)
    with app.app_context():
        settings.init_app()  # Run early on to load configuration.
        security = auth.init_app()
        for code in (403, 404, 500):
            app.register_error_handler(code, error_handler(code))

    @app.route("/")
    def root() -> Response:
        # noinspection PyUnresolvedReferences
        return app.redirect(app.url_for("home"))

    @app.route("/home")
    def home() -> Response:
        # noinspection PyUnresolvedReferences
        return app.redirect(security.login_url)

    @app.route("/inbox", methods=["GET", "POST"])
    @fs.auth_required()
    def inbox() -> str | Response:
        get = flask.request.method == "GET"
        emails = get_emails()
        delete = forms.DeleteEmailsForm(emails)
        compose = forms.ComposeEmailForm(security.datastore)
        if not get and delete.validate_on_submit():
            result = delete_emails(delete, emails)
        # Only validate if the POST request is actually to send an email.
        elif not get and in_form("subject") and compose.validate_on_submit():
            result = compose_email(compose)
        else:
            result = render_template(
                "inbox.html",
                emails=list(zip(emails, delete.emails)),
                delete=delete,
                compose=compose,
                current_user=current_user())
        return result

    return app


def get_emails() -> list[models.Email]:
    # Emails should be returned in a consistent order to delete them.
    emails = models.Email.get(current_user())
    return sorted(emails, key=lambda e: e.headers.date, reverse=True)


def compose_email(form: forms.ComposeEmailForm) -> Response:
    email = models.Email(
        headers=models.EmailHeaders(
            to=form.to.data,
            sender=current_user_address(),
            subject=form.subject.data),
        body=form.body.data)
    email.save(form.username)
    return redirect_to_inbox()


def delete_emails(
        form: forms.DeleteEmailsForm,
        emails: Iterable[models.Email]
) -> Response:
    models.Email.delete_all(e for e in emails if e.uid in form.emails.data)
    return redirect_to_inbox()


def error_handler(code: int) -> ErrorHandlerCallable:
    return lambda e: (render_template(f"{code}.html"), code)


def redirect_to_inbox() -> Response:
    return flask.current_app.redirect(flask.url_for("inbox"))


def in_form(field: str) -> bool:
    return field in flask.request.form


def render_template(path: str, **context) -> str:
    path = os.path.join(flask.current_app.config.PAGES_DIR, path)
    return flask.render_template(path, **context)


def current_user_address() -> EmailStr:
    return forms.format_address(current_user())


def current_user() -> str:
    return fs.current_user.username


def hat_client() -> client.HatClient:
    return flask.current_app.config.HAT_CLIENT
