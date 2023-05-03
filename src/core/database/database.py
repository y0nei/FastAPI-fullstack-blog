from datetime import datetime
from src.core.logging import logger
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_route_views(route: str, db: AsyncIOMotorDatabase) -> dict[str, int]:
    collection = db["views"]
    pipeline = [{"$match": {"routes": route}}, {"$count": "views"}]
    cursor = collection.aggregate(pipeline)
    try:
        item = await cursor.next()
    except StopAsyncIteration:
        return {"views": 0}
    return item

async def add_view(route: str, ssid: str, db: AsyncIOMotorDatabase) -> None:
    collection = db["views"]
    document = await collection.find_one({"ssid": ssid, "routes": route})
    if document:
        logger.debug(f"Route {route} in ssid={ssid} already exists")
        return

    result = await collection.update_one({"ssid": ssid}, {
        "$addToSet": {"routes": route},
        "$setOnInsert": {"timestamps.added": datetime.utcnow()},
        "$set": {"timestamps.last_modified": datetime.utcnow()}
    }, upsert=True)

    if result.upserted_id:
        logger.debug(f"New document created for ssid={ssid}")
    elif result.modified_count > 0:
        logger.debug(f"Document updated for ssid={ssid}")
