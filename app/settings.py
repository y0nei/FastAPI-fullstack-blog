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
    SECRET_KEY: str = "supersecret"

    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 27017

    MONGO_DATABASE: str = "database"
    MONGO_COLLECTION: str = "collection"

    class Config:
        env_file = ".env"

settings: Settings = Settings()
