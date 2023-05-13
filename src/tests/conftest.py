import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from src.app import app
from src.core.settings import settings
from src.core.database.session import DataBase
from mongomock_motor import AsyncMongoMockClient
from starlette.middleware.sessions import SessionMiddleware

# Override setting for cookie creation
settings.POST_STATISTICS = True

mongoclient = AsyncMongoMockClient()

async def get_mock_db():
    return mongoclient["someDB"]

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
    app.dependency_overrides[DataBase().get_database] = get_mock_db
    app.add_middleware(SessionMiddleware, secret_key="random_string")

    async with AsyncClient(app=app, base_url="http://test") as _client:
        await _client.get("/createsession")  # Create cookie session
        yield _client
