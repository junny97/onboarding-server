import os
from typing import Optional, Dict, Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정"""
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./onboarding.db"
    PROJECT_NAME: str = "온보딩 API"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 