from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Voice AI Patient Registration"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    database_url: str = "sqlite:///./voice_patient.db"
    vapi_api_key: str | None = None
    vapi_webhook_secret: str | None = None
    vapi_assistant_id: str | None = None
    vapi_phone_number_id: str | None = None
    public_base_url: str = "http://localhost:8000"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
