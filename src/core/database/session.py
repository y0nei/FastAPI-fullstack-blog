from src.core.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class DataBase:
    _instance = None
    client: AsyncIOMotorClient | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if settings.POST_STATISTICS:
                cls._instance.client = AsyncIOMotorClient(settings.DB_URL)
        return cls._instance

    def get_database(self) -> AsyncIOMotorDatabase:
        if self.client is not None:
            return self.client[settings.DB_NAME]
