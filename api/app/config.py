"""Application configuration via pydantic-settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://f2f:f2f@db:5432/f2f"
    redis_url: str = "redis://redis:6379/0"

    s3_endpoint: str = "http://minio:9000"
    s3_bucket: str = "f2f-assets"
    s3_access_key: str = "f2fminio"
    s3_secret_key: str = "f2fminio-secret"  # noqa: S105 — local-dev default; prod secrets come from .env

    tripo_api_key: str = ""
    tripo_api_base: str = "https://api.tripo3d.ai"


@lru_cache
def get_settings() -> Settings:
    return Settings()
