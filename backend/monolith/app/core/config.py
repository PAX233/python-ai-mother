from functools import lru_cache

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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
