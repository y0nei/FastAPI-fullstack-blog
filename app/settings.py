from pydantic import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False

    class Config:
        env_file = ".env"
