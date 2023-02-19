from enum import Enum
from pydantic import BaseSettings

class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    DEBUG: int = 1
    ENVIROMENT: EnvType = EnvType.DEVELOPMENT

    class Config:
        env_file = ".env"

settings: Settings = Settings()
