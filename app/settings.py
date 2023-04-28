import logging
from enum import Enum
from pydantic import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient

class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    LOG_LEVEL: str = "info"
    ENVIRONMENT: str = EnvType.DEVELOPMENT
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    HOTRELOAD: bool = False
    ENABLE_METRICS: bool = False
    SECRET_KEY: str = "supersecret"

    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 27017

    MONGO_DATABASE: str = "database"
    MONGO_COLLECTION: str = "collection"

    @property
    def DB_URL(self) -> str:
        return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}"

    class Config:
        env_file = ".env"

settings: Settings = Settings()

async def get_prod_db():
    return AsyncIOMotorClient(settings.DB_URL)[settings.MONGO_DATABASE][settings.MONGO_COLLECTION]

# TODO: Temporarely store this here
logger = logging.getLogger("uvicorn.error")
