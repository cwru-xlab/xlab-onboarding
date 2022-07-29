from __future__ import annotations

import datetime

import humps.main as pyhumps
from pydantic import (BaseModel, EmailStr, Field, StrictStr, constr)


def list_field(
        unique_items: bool = True,
        min_items: int = 0,
        max_items: int | None = None
) -> Field:
    return Field(
        unique_items=unique_items,
        min_items=min_items,
        max_items=max_items,
        default_factory=list)


def datetime_field() -> Field:
    return Field(default_factory=datetime.datetime.utcnow)


def title_kebab(s: str) -> str:
    return pyhumps.kebabize(s).title()


class EmailModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        allow_mutation = False


class EmailHeader(EmailModel):
    to: list[EmailStr] = list_field(min_items=1)
    cc: list[EmailStr] = list_field()
    sender: EmailStr
    reply_to: EmailStr
    return_path: EmailStr
    subject: constr(strip_whitespace=True, strict=True) = ""
    date: datetime.datetime = datetime_field()

    class Config(EmailModel.Config):
        alias_generator = title_kebab
        fields = {"sender": title_kebab("from"), "cc": "CC", "bcc": "BCC"}

    def dict(self, by_alias: bool = True, **kwargs):
        return super().dict(by_alias=by_alias, **kwargs)

    def json(self, by_alias: bool = True, **kwargs):
        return super().json(by_alias=by_alias, **kwargs)


class EmailEnvelope(EmailModel):
    pass


class Email(EmailModel):
    header: EmailHeader
    envelope: EmailEnvelope
    body: StrictStr


SCHEMA = {"*": Email}
