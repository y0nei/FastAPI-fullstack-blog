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
    APP_NAME: str = "FastAPI Blog"
    LOG_LEVEL: str = "info"
    ENVIRONMENT: str = EnvType.DEVELOPMENT
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    HOTRELOAD: bool = False
    POST_STATISTICS: bool = False
    ENABLE_METRICS: bool = False
    SECRET_KEY: str | None = None

class DatabaseSettings(BaseConfig):
    if AppSettings().POST_STATISTICS:
        DB_USER: str
        DB_PASSWORD: str
        DB_HOST: str
        DB_PORT: int = 27017
        DB_NAME: str

        @property
        def DB_URL(self) -> str:
            return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}"
    else:
        pass

class Settings(AppSettings, DatabaseSettings):
    pass

settings: Settings = Settings()
