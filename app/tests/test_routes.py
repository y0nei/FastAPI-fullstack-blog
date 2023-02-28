from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

def test_home_route():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

def test_valid_post_route_item():
    response = client.get("/post/1")
    assert response.status_code == status.HTTP_200_OK

def test_empty_post_route_item():
    response = client.get("/post/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_invalid_post_route_item():
    non_int_value = client.get("/post/foo")
    negative_value = client.get("/post/-1")
    assert non_int_value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert negative_value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
