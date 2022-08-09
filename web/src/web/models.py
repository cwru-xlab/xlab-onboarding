import datetime

import hat
import pydantic
from pydantic import EmailStr, StrictStr, constr


def datetime_field() -> pydantic.Field:
    return pydantic.Field(default_factory=datetime.datetime.utcnow)


class EmailHeaders(pydantic.BaseModel):
    to: EmailStr
    sender: EmailStr
    subject: constr(strip_whitespace=True, strict=True)
    date: datetime.datetime = datetime_field()

    class Config(hat.HatConfig):
        fields = {"sender": "from"}


class Email(hat.ActiveHatModel):
    headers: EmailHeaders
    body: StrictStr
