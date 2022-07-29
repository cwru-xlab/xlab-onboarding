from pydantic import BaseSettings, StrictStr


class Config(BaseSettings):
    domain: StrictStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        allow_mutation = False


config = Config()
