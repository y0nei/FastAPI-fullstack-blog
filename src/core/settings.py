from enum import Enum
from pydantic import BaseSettings

class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True

class AppSettings(BaseConfig):
    LOG_LEVEL: str = "info"
    ENVIRONMENT: str = EnvType.DEVELOPMENT
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    HOTRELOAD: bool = False
    ENABLE_METRICS: bool = False
    SECRET_KEY: str = "supersecret"

class DatabaseSettings(BaseConfig):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 27017
    MONGO_DATABASE: str = "database"

    @property
    def DB_URL(self) -> str:
        return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}"

class Settings(AppSettings, DatabaseSettings):
    pass

settings: Settings = Settings()
