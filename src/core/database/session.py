from src.core.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

async def get_prod_db():
    return AsyncIOMotorClient(settings.DB_URL)[settings.MONGO_DATABASE][settings.MONGO_COLLECTION]
