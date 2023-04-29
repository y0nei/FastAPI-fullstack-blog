from datetime import datetime
from fastapi import Request
from src.core.logging import logger
from motor.motor_asyncio import AsyncIOMotorCollection

async def get_route_views(route: str, collection: AsyncIOMotorCollection) -> dict[str, int]:
    pipeline = [{"$match": {"routes": route}}, {"$count": "views"}]
    cursor = collection.aggregate(pipeline)
    try:
        item = await cursor.next()
    except StopAsyncIteration:
        return {"views": 0}
    return item

async def add_view(request: Request, collection: AsyncIOMotorCollection):
    ssid = request.session.get("ssid")
    if not ssid:
        logger.debug(f"Ssid not found, ssid={ssid}")
        return

    # Check if the current route is already present in the database
    document = await collection.find_one({"ssid": ssid, "routes": request.url.path})
    if document:
        logger.debug(f"Route {request.url.path} in ssid={ssid} already exists")
        return

    # Store the current route in the database or create new entry
    update = {
        "$addToSet": {"routes": request.url.path},
        "$setOnInsert": {"timestamps.added": datetime.utcnow()},
    }
    result = await collection.update_one({"ssid": ssid}, update, upsert=True)

    if result.upserted_id:
        # The document was inserted, add missing fields
        await collection.update_one(
            {"_id": result.upserted_id},
            {"$currentDate": {"timestamps.last_modified": True}}
        )
        logger.debug(f"New document created for ssid={ssid}")
    else:
        # Check if the routes field was updated
        if result.modified_count > 0:
            await collection.update_one(
                {"ssid": ssid},
                {"$currentDate": {"timestamps.last_modified": True}}
            )
            logger.debug(f"Document updated for ssid={ssid}")
