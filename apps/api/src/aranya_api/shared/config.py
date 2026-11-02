from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/aranya"
    session_secret: str = "development-only-secret-change-before-production"
    web_origin: str = "http://localhost:3000"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    ai_low_confidence_threshold: float = 0.70
    hold_duration_minutes: int = 15
    rate_currency: str = "INR"
    gst_rate_percentage: float = 18.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
