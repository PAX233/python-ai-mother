from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "python-ai-mother-backend"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    debug: bool = False
    log_level: str = "INFO"
    cors_origins: str = "*"
    database_url: str = "sqlite+aiosqlite:///./python_ai_mother.db"
    redis_url: str = "redis://localhost:6379/0"
    password_salt: str = "python-ai-mother"
    session_cookie_name: str = "python_ai_mother_sid"
    session_ttl_seconds: int = 86400
    session_cookie_secure: bool = False
    session_cookie_samesite: str = "lax"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        normalized = value.strip().lower()
        if normalized in {"release", "prod", "production", "false", "0", "off", "no"}:
            return False
        if normalized in {"debug", "dev", "development", "true", "1", "on", "yes"}:
            return True
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
