from __future__ import annotations

from typing import Iterable

import flask
import flask_security as fs
import flask_wtf
import pydantic
import wtforms
from flask_security import UserDatastore
from wtforms import validators, widgets

from models import Email


class UsernameRegisterForm(fs.RegisterForm):
    """Hack to utilize RegisterForm, but use username instead of email."""

    email = fs.forms.EmailField()  # Default: no validation


# Ref: https://gist.github.com/ectrimble20/468156763a1389a913089782ab0f272e
class MultiCheckboxField(wtforms.SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class DeleteEmailsForm(flask_wtf.FlaskForm):
    emails = MultiCheckboxField()
    submit = wtforms.SubmitField("Delete")

    def __init__(self, emails: Iterable[Email], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emails.choices = [e.uid for e in emails]

    def validate_on_submit(self, *args, **kwargs):
        if result := super().validate(*args, **kwargs):
            result = bool(self.emails.data)
        return result


class ComposeEmailForm(flask_wtf.FlaskForm):
    to = wtforms.EmailField(validators=[validators.DataRequired()])
    subject = wtforms.StringField(
        default="(No subject)", validators=[validators.DataRequired()])
    body = wtforms.TextAreaField()
    submit = wtforms.SubmitField("Send")

    def __init__(self, users: UserDatastore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = users

    def validate(self, *args, **kwargs):
        if result := super().validate(*args, **kwargs):
            domain = flask.current_app.config.EMAIL_DOMAIN
            if not (result := self.domain == domain):
                self.to.errors.append(f"Email domain must be {domain}")
            elif not (result := self.users.find_user(username=self.username)):
                self.to.errors.append(f"{self.to.data} does not exist")
        return result

    @property
    def username(self) -> str:
        return self.to.data.split("@")[0]

    @property
    def domain(self) -> str:
        return self.to.data.split("@")[-1]


def format_address(username: str) -> pydantic.EmailStr:
    domain = flask.current_app.config.EMAIL_DOMAIN
    return pydantic.EmailStr(f"{username}@{domain}")
