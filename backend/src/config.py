from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    BETTER_AUTH_SECRET: str = "your-secret-key"
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "your-frontend-key"
    FRONTEND_URL2: str = "your-frontend-key"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"

    # Additional settings for different environments
    DEBUG: bool = False
    TESTING: bool = False

    class Config:
        env_file = ".env"


settings = Settings()