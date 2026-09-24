from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "dhcp-manager-api"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://dhcp_manager:dhcp_manager@db:5432/dhcp_manager"
    redis_url: str = "redis://redis:6379/0"
    deployment_execution_enabled: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DHCP_MANAGER_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
