from fastapi import status

# TODO: Handle testing route status codes better / in a single test
def test_home_route(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

def test_valid_post_route_item(client):
    response = client.get("/posts/1")
    assert response.status_code == status.HTTP_200_OK

def test_empty_post_route_item(client):
    response = client.get("/posts/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_invalid_post_route_item(client):
    non_int_value = client.get("/posts/foo")
    negative_value = client.get("/posts/-1")
    assert non_int_value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert negative_value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_post_list_request_headers(client):
    """
    Checks if the '/posts' endpoint returns proper hx-request and content-type header
    when the 'hx-request' header is specified.
    """
    # hx-response
    hx_response = client.get("/posts", headers={"hx-request": "foo"})
    assert hx_response.request.headers.__contains__("hx-request") is True
    assert hx_response.request.headers.get("hx-request") == "foo"
    assert hx_response.headers.get("content-type") == "text/html; charset=utf-8"
    # json response
    json_response = client.get("/posts")
    assert json_response.request.headers.__contains__("hx-request") is False
    assert json_response.headers.get("content-type") == "application/json"
