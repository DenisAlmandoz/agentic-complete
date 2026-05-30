from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:8000"

    xai_api_key: str = Field(default="", repr=False)
    xai_base_url: str = "https://api.x.ai/v1"
    grok_model: str = "grok-4.3"
    embedding_model: str = "text-embedding-3-small"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "language_tutor"
    mongodb_memory_collection: str = "memories"
    mongodb_knowledge_collection: str = "knowledge"
    mongodb_vector_index: str = "vector_index"

    langfuse_public_key: str = ""
    langfuse_secret_key: str = Field(default="", repr=False)
    langfuse_host: str = "https://cloud.langfuse.com"

    whisper_model: str = "base"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
