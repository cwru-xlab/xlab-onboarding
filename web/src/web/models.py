import datetime

import pydantic
from pydantic import NameEmail, StrictStr, constr


def datetime_field() -> pydantic.Field:
    return pydantic.Field(default_factory=datetime.datetime.utcnow)


class EmailModel(pydantic.BaseModel):
    class Config:
        allow_population_by_field_name = True
        allow_mutation = False


class EmailHeaders(EmailModel):
    to: NameEmail
    sender: NameEmail
    subject: constr(strip_whitespace=True, strict=True)
    date: datetime.datetime = datetime_field()

    class Config(EmailModel.Config):
        fields = {"sender": "from"}


class Email(EmailModel):
    headers: EmailHeaders
    body: StrictStr
