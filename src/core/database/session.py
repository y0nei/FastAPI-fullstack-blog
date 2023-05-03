from src.core.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class DataBase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = AsyncIOMotorClient(settings.DB_URL)
        return cls._instance

    def get_database(self) -> AsyncIOMotorDatabase:
        return self.client[settings.MONGO_DATABASE]

    def get_client(self) -> AsyncIOMotorClient:
        return self.client

database = DataBase()