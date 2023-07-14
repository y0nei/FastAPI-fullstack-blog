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

# TODO: Move this out of here into a TOML file later
short_description = "A python-based blogging framework designed to simplify \
content management with Markdown parsing, database integration, and other \
interactive features."

app_description = """
A Python application designed to serve as a personal blogging framework.

It parses Markdown files organized into numbered folders to generate an easy
navigable list of articles.  
Thanks to the power of [**FastAPI**][1] and various [**Markdown addons**][2],
it simplifies the process of building and managing blogs.

This app also provides optional database integration for storing article views,
Prometheus metrics for monitoring, [**hot reloading**][3] for efficient
development and an interactive article listing thanks to the use of the
[**HTMX JavaScript framework**][4].

[1]: https://fastapi.tiangolo.com/
[2]: https://gitlab.com/yonei.dev/fullstack/-/blob/main/pyproject.toml#L19
[3]: https://github.com/florimondmanca/arel
[4]: https://htmx.org/
"""
