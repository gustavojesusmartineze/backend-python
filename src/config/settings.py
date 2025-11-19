from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
import os


class Settings(BaseSettings):
    """
    Global application settings loaded from environment variables.

    This is used by:
        - FastAPI app
        - Alembic env.py
        - Database connection engine
        - External service adapters
    """

    model_config = SettingsConfigDict(
        env_file=".env",            # Load from .env automatically
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # ------------------------------------------------------------
    # APPLICATION SETTINGS
    # ------------------------------------------------------------
    APP_ENV: str = Field(default="development")
    APP_NAME: str = Field(default="EdTech Platform API")
    APP_DEBUG: bool = Field(default=True)

    # ------------------------------------------------------------
    # DATABASE CONFIG
    # ------------------------------------------------------------
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_NAME: str = Field(default="edtech_db")

    # Fully assembled SQLAlchemy URL
    DATABASE_URL: str = ""
    
    DB_ECHO: bool = False

    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_database_url(cls, v, values):
        """
        Build SQLAlchemy-compatible DB URL if not provided directly.
        """
        if v and v.strip():
            return v

        user = values.get("DB_USER")
        pwd = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        db = values.get("DB_NAME")

        return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"


# Global settings instance (import anywhere)
settings = Settings()
