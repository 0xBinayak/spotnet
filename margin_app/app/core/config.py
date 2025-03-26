"""
Core configuration settings for the application.
"""

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from typing import Optional


class Settings(BaseSettings):
    """Configuration settings for the application."""

    # Application settings
    app_env: str = "development"
    secret_key: str = "SECRET_KEY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database settings
    db_driver: str = "postgresql+asyncpg"
    db_name: str = Field(default="db_name", alias="POSTGRES_DB")
    db_user: str = Field(default="user", alias="POSTGRES_USER")
    db_password: str = Field(default="password", alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = 5432

    # Email settings
    sendgrid_api_key: Optional[str] = Field(alias="SENDGRID_API_KEY")
    email_sender: Optional[str] = Field(alias="EMAIL_SENDER")
    email_sender_name: Optional[str] = Field(alias="EMAIL_SENDER_NAME")
    email_test_mode: bool = Field(default=False, alias="EMAIL_TEST_MODE")

    @computed_field
    @property
    def db_url(self) -> URL:
        """
        Computed property to get SQLAlchemy URL, using env settings
        """
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            database=self.db_name,
            port=self.db_port,
        )


settings = Settings()
