import logging
from functools import lru_cache
from typing import Any, cast

from pydantic import BaseSettings, PostgresDsn, validator

logger = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    ENV_NAME: str = "default_env"
    DB_NAME: str = "default_db"
    DB_USER: str = "default_user"
    DB_PASS: str = "default_pass"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_URL: str = ""
    JWT_REFRESH_SECRET_KEY: str
    JWT_ACCESS_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES_IN: str
    JWT_REFRESH_TOKEN_EXPIRES_IN: str
    JWT_ALGORITHM: str
    SQL_SHOW_QUERY: bool = False

    @validator("DB_URL", pre=True)
    def get_database_url(cls, v: str | None, values: dict[str, Any]) -> str:
        if isinstance(v, str) and v:
            return v
        result = cast(
            str,
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values.get("DB_USER"),
                password=values.get("DB_PASS"),
                host=values.get("DB_HOST"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME')}",
            ),
        )
        return result

    class Config:
        env_file = ".env", "../.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_app_settings() -> AppSettings:
    settings = AppSettings()  # type: ignore
    logger.info(f">>> Loading settings for: {settings.ENV_NAME}\n")
    return settings
