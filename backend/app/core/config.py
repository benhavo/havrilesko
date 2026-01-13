from functools import lru_cache
from typing import Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pytimeparse import parse


class Settings(BaseSettings):
    # Environment
    environment: Literal["local", "production", "test"] = "local"
    debug: bool = False

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v):
        """Handle empty strings and various boolean representations"""
        if v == "" or v is None:
            return False
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "havrilesko"
    db_user: str = "postgres"
    db_password: str = ""

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # Security
    secret_key: str = "insecure-dev-key-change-in-production"

    # JWT RSA Keys
    rsa_private_key: str

    @field_validator("rsa_private_key", mode="before")
    @classmethod
    def decode_rsa_key(cls, v):
        """Handle base64 encoded keys from env vars"""
        if v and not v.startswith("-----BEGIN"):
            import base64

            return base64.b64decode(v).decode("utf-8")
        return v

    # JWT Configuration
    jwt_algorithm: str = "RS256"
    jwt_ttl_access: str = "5 minutes"
    jwt_ttl_refresh: str = "30 days"
    jwt_issuer_domain: str = "localhost:8000"

    @property
    def jwt_ttl_access_seconds(self) -> int:
        return parse(self.jwt_ttl_access) or 300

    @property
    def jwt_ttl_refresh_seconds(self) -> int:
        return parse(self.jwt_ttl_refresh) or 2592000

    # CORS
    frontend_domain: str = "localhost:3000"
    backend_domain: str = "localhost:8000"
    cors_origins: list[str] = ["http://localhost:3000", "https://localhost:3000"]

    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Havrilesko API"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
