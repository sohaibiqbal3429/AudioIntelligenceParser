from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    whisper_model: str = Field(default="base", alias="WHISPER_MODEL")
    max_upload_size_bytes: int = Field(default=25 * 1024 * 1024, alias="MAX_UPLOAD_SIZE_BYTES")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
