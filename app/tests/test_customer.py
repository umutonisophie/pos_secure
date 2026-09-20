import pytest
from fastapi import status


def test_list_customers(client, auth_headers):
    response = client.get("/customers", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_customer(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    response = client.post("/customers", json=customer_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data


def test_create_customer_missing_first_name(client, auth_headers):
    customer_data = {
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    response = client.post("/customers", json=customer_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_customer_missing_last_name(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "email": "john.doe@example.com"
    }
    response = client.post("/customers", json=customer_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_customer(client, auth_headers):
    customer_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
    }
    create_response = client.post("/customers", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]

    response = client.get(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["email"] == "jane.smith@example.com"
    assert data["id"] == customer_id


def test_get_nonexistent_customer(client, auth_headers):
    response = client.get("/customers/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Customer not found"


def test_update_customer(client, auth_headers):
    customer_data = {
        "first_name": "Old",
        "last_name": "Name",
        "email": "old@example.com"
    }
    create_response = client.post("/customers", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]

    update_data = {
        "first_name": "New",
        "last_name": "Name",
        "email": "new@example.com"
    }
    response = client.put(f"/customers/{customer_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "New"
    assert data["last_name"] == "Name"
    assert data["email"] == "new@example.com"


def test_update_customer_partial(client, auth_headers):
    customer_data = {
        "first_name": "Partial",
        "last_name": "Update",
        "email": "partial@example.com"
    }
    create_response = client.post("/customers", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]

    update_data = {"email": "updated@example.com"}
    response = client.put(f"/customers/{customer_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Partial"
    assert data["last_name"] == "Update"
    assert data["email"] == "updated@example.com"


def test_update_nonexistent_customer(client, auth_headers):
    response = client.put("/customers/999", json={"first_name": "Test"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_customer(client, auth_headers):
    customer_data = {
        "first_name": "To",
        "last_name": "Delete",
        "email": "delete@example.com"
    }
    create_response = client.post("/customers", json=customer_data, headers=auth_headers)
    customer_id = create_response.json()["id"]

    response = client.delete(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/customers/{customer_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_customer(client, auth_headers):
    response = client.delete("/customers/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_customers_without_auth(client):
    response = client.get("/customers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED