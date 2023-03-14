from enum import Enum
from pydantic import BaseSettings

class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    DEBUG: int = 1
    ENVIRONMENT: str = EnvType.DEVELOPMENT
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"

settings: Settings = Settings()
