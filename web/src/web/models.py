import datetime

import hat
import pydantic
from pydantic import NameEmail, StrictStr, constr


def datetime_field() -> pydantic.Field:
    return pydantic.Field(default_factory=datetime.datetime.utcnow)


class EmailConfig(pydantic.BaseConfig):
    allow_population_by_field_name = True


class EmailHeaders(pydantic.BaseModel):
    to: NameEmail
    sender: NameEmail
    subject: constr(strip_whitespace=True, strict=True)
    date: datetime.datetime = datetime_field()

    class Config(EmailConfig):
        fields = {"sender": "from"}


class Email(hat.ActiveHatModel):
    headers: EmailHeaders
    body: StrictStr

    Config = EmailConfig
