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

    def __init__(self, users: UserDatastore, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.users = users

    def validate(self, *args, **kwargs) -> bool:
        if result := super().validate(*args, **kwargs):
            if not (result := self.recipient_domain == (expected := email_domain())):
                self.to.errors.append(f"Email domain must be {expected}")
            elif not (result := self.users.find_user(username=self.recipient_username)):
                self.to.errors.append(f"{self.to.data} does not exist")
        return result

    @property
    def recipient_username(self) -> str:
        return self.to.data.split("@")[0]

    @property
    def recipient_domain(self) -> str:
        return self.to.data.split("@")[1]


def format_address(username: str) -> pydantic.EmailStr:
    return pydantic.EmailStr(f"{username}@{email_domain()}")


def email_domain() -> str:
    return flask.current_app.config.EMAIL_DOMAIN
