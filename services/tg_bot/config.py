from typing import Annotated

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMIN_IDS: Annotated[set[int], NoDecode]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def decode_numbers(cls, v: str) -> set[int]:
        return {int(x) for x in v.split(",")}


settings = Settings()
