import datetime
from typing import Optional

import pydantic
from hat import client, model
from pydantic import EmailStr, StrictStr, constr


def datetime_field() -> pydantic.Field:
    return pydantic.Field(default_factory=datetime.datetime.utcnow)


class EmailHeaders(pydantic.BaseModel):
    to: EmailStr
    sender: EmailStr
    subject: constr(strip_whitespace=True, strict=True)
    date: datetime.datetime = datetime_field()

    Config = model.HatConfig

    @property
    def short_date(self) -> str:
        # Old: Aug 12. Otherwise: Tue 1:23 PM
        return self.date.strftime("%b %d" if self._old() else "%a %I:%M %p")

    @property
    def full_date(self) -> str:
        # Old: Tue Aug 12 – 1:23 PM. Otherwise: Tue 1:23 PM
        return self.date.strftime(
            "%a %b %d – %I:%M %p" if self._old() else "%a %I:%M %p")

    def _old(self) -> bool:
        age = datetime.datetime.utcnow() - self.date
        return age >= datetime.timedelta(weeks=1)


class Email(client.ActiveHatModel):
    headers: EmailHeaders
    body: Optional[StrictStr]
