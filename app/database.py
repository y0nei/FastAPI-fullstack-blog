import uuid
from fastapi import Request
from app.settings import settings
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
)
database = client[settings.MONGO_DATABASE]
collection = database[settings.MONGO_COLLECTION]

async def get_route_views(id: int) -> dict[str, int]:
    pipeline = [{"$match": {"routes": f"/posts/{id}"}}, {"$count": "views"}]
    cursor = collection.aggregate(pipeline)
    try:
        item = await cursor.next()
    except StopAsyncIteration:
        return {"views": 0}  # TODO: Catch an error here
    return item

async def add_view(request: Request):
    ssid = request.session.get("ssid")
    # Create a new session if one does not exist
    if not ssid:
        ssid = str(uuid.uuid4())
        request.session["ssid"] = ssid
    # Store the current route in the database or create new entry
    result = await collection.update_one(
        {"ssid": ssid},
        {"$addToSet": {"routes": request.url.path}}
    )
    if result.matched_count == 0:
        await collection.insert_one({"ssid": ssid, "routes": [request.url.path]})
