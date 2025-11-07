"""Application configuration settings."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://invest:invest@localhost:5432/investdb"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    secret_key: str = os.getenv("SECRET_KEY", "dev")
    env: str = os.getenv("ENV", "dev")
    polygon_api_key: str | None = os.getenv("POLYGON_API_KEY")
    newsapi_api_key: str | None = os.getenv("NEWSAPI_API_KEY")
    finbert_model: str = os.getenv("FINBERT_MODEL", "ProsusAI/finbert")


settings = Settings()
