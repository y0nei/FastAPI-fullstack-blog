import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from app.api import app
from app.database import get_prod_db
from mongomock_motor import AsyncMongoMockClient

mongoclient = AsyncMongoMockClient()

async def get_mock_db():
    db = mongoclient["someDB"]
    collection = db["someCollection"]
    return collection

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture()
async def get_db():
    return await get_mock_db()

@pytest_asyncio.fixture(scope="session")
async def client():
    app.dependency_overrides[get_prod_db] = get_mock_db

    async with AsyncClient(app=app, base_url="http://test") as _client:
        yield _client
