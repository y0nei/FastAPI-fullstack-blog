import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.database import get_prod_db
from mongomock_motor import AsyncMongoMockClient

mongoclient = AsyncMongoMockClient()

async def get_mock_db():
    db = mongoclient["someDB"]
    collection = db["someCollection"]
    return collection

@pytest.fixture()
async def get_db():
    return await get_mock_db()

@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_prod_db] = get_mock_db

    with TestClient(app) as _client:
        yield _client
