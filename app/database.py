from datetime import datetime
from fastapi import Request
from app.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

# TODO: move those database variables out of this file
client = AsyncIOMotorClient(
    f"mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
)
database = client[settings.MONGO_DATABASE]
my_collection = database[settings.MONGO_COLLECTION]

async def get_prod_db():
    return my_collection

async def get_route_views(route: str, collection: AsyncIOMotorCollection) -> dict[str, int]:
    pipeline = [{"$match": {"routes": route}}, {"$count": "views"}]
    cursor = collection.aggregate(pipeline)
    try:
        item = await cursor.next()
    except StopAsyncIteration:
        return {"views": 0}  # TODO: Catch an error here
    return item

async def add_view(request: Request, collection: AsyncIOMotorCollection):
    ssid = request.session.get("ssid")
    if not ssid:
        print("ssid not found", f"ssid={ssid}") if settings.DEBUG else None
        return

    # Check if the current route is already present in the database
    document = await collection.find_one({"ssid": ssid, "routes": request.url.path})
    if document:
        return  # Route already exists, nothing to do

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
        print(f"New document created for ssid={ssid}") if settings.DEBUG else None
    else:
        # Check if the routes field was updated
        if result.modified_count > 0:
            await collection.update_one(
                {"ssid": ssid},
                {"$currentDate": {"timestamps.last_modified": True}}
            )
            print(f"Document updated for ssid={ssid}") if settings.DEBUG else None
