import pytest
from fastapi import status


def test_list_categories(client, auth_headers):
    response = client.get("/categories", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_category(client, auth_headers):
    category_data = {
        "name": "Beverages",
        "description": "Drinks and beverages"
    }
    response = client.post("/categories", json=category_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Beverages"
    assert data["description"] == "Drinks and beverages"
    assert "id" in data


def test_create_category_missing_name(client, auth_headers):
    category_data = {
        "description": "Missing name"
    }
    response = client.post("/categories", json=category_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_category(client, auth_headers):
    category_data = {"name": "Electronics", "description": "Electronic devices"}
    create_response = client.post("/categories", json=category_data, headers=auth_headers)
    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Electronics"
    assert data["description"] == "Electronic devices"
    assert data["id"] == category_id


def test_get_nonexistent_category(client, auth_headers):
    response = client.get("/categories/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Category not found"


def test_update_category(client, auth_headers):
    category_data = {"name": "Old Name", "description": "Old description"}
    create_response = client.post("/categories", json=category_data, headers=auth_headers)
    category_id = create_response.json()["id"]

    update_data = {"name": "New Name", "description": "New description"}
    response = client.put(f"/categories/{category_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "New description"


def test_update_category_partial(client, auth_headers):
    category_data = {"name": "Partial Update", "description": "Will update name only"}
    create_response = client.post("/categories", json=category_data, headers=auth_headers)
    category_id = create_response.json()["id"]

    update_data = {"name": "Updated Name"}
    response = client.put(f"/categories/{category_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Will update name only"


def test_update_nonexistent_category(client, auth_headers):
    response = client.put("/categories/999", json={"name": "Test"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_category(client, auth_headers):
    category_data = {"name": "To Delete", "description": "Will be deleted"}
    create_response = client.post("/categories", json=category_data, headers=auth_headers)
    category_id = create_response.json()["id"]

    response = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_category(client, auth_headers):
    response = client.delete("/categories/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_categories_without_auth(client):
    response = client.get("/categories")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED