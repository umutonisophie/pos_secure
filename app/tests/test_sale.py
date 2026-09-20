import pytest
from fastapi import status
from decimal import Decimal


def test_list_sales(client, auth_headers):
    response = client.get("/sales", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_sale(client, auth_headers, test_user):
    # First create a user to use as the sales person
    user_response = client.post("/auth/register", json={
        "username": "salesuser",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_data = {
        "total_amount": "100.50",
        "customer_id": None,
        "user_id": user_id
    }
    response = client.post("/sales", json=sale_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert float(data["total_amount"]) == 100.50
    assert data["user_id"] == user_id
    assert data["customer_id"] is None
    assert "id" in data
    assert "sale_date" in data


def test_create_sale_with_customer(client, auth_headers, test_user):
    # Create a customer first
    cust_response = client.post("/customers", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }, headers=auth_headers)
    customer_id = cust_response.json()["id"]

    # Create a user for the sale
    user_response = client.post("/auth/register", json={
        "username": "salesuser2",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_data = {
        "total_amount": "200.00",
        "customer_id": customer_id,
        "user_id": user_id
    }
    response = client.post("/sales", json=sale_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert float(data["total_amount"]) == 200.00
    assert data["customer_id"] == customer_id
    assert data["user_id"] == user_id


def test_create_sale_missing_total_amount(client, auth_headers):
    sale_data = {
        "customer_id": None,
        "user_id": 1
    }
    response = client.post("/sales", json=sale_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_sale_missing_user_id(client, auth_headers):
    sale_data = {
        "total_amount": "100.00",
        "customer_id": None
    }
    response = client.post("/sales", json=sale_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_sale_invalid_user_id(client, auth_headers):
    sale_data = {
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": 999
    }
    response = client.post("/sales", json=sale_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User" in response.json()["detail"]


def test_create_sale_invalid_customer_id(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "salesuser3",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_data = {
        "total_amount": "100.00",
        "customer_id": 999,
        "user_id": user_id
    }
    response = client.post("/sales", json=sale_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Customer" in response.json()["detail"]


def test_get_sale(client, auth_headers, test_user):
    user_response = client.post("/auth/register", json={
        "username": "salesuser4",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_data = {
        "total_amount": "150.00",
        "customer_id": None,
        "user_id": user_id
    }
    create_response = client.post("/sales", json=sale_data, headers=auth_headers)
    sale_id = create_response.json()["id"]

    response = client.get(f"/sales/{sale_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert float(data["total_amount"]) == 150.00
    assert data["user_id"] == user_id
    assert data["id"] == sale_id


def test_get_nonexistent_sale(client, auth_headers):
    response = client.get("/sales/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Sale not found"


def test_update_sale(client, auth_headers, test_user):
    user_response = client.post("/auth/register", json={
        "username": "salesuser5",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_data = {
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }
    create_response = client.post("/sales", json=sale_data, headers=auth_headers)
    sale_id = create_response.json()["id"]

    update_data = {
        "total_amount": "200.00"
    }
    response = client.put(f"/sales/{sale_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert float(data["total_amount"]) == 200.00


def test_update_sale_partial(client, auth_headers, test_user):
    user_response = client.post("/auth/register", json={
        "username": "salesuser6",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    # Create a customer to assign to the sale
    cust_response = client.post("/customers", json={
        "first_name": "Test",
        "last_name": "Customer",
        "email": "test.customer@example.com"
    }, headers=auth_headers)
    customer_id = cust_response.json()["id"]

    sale_data = {
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }
    create_response = client.post("/sales", json=sale_data, headers=auth_headers)
    sale_id = create_response.json()["id"]

    update_data = {"customer_id": customer_id}
    response = client.put(f"/sales/{sale_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["customer_id"] == customer_id


def test_update_nonexistent_sale(client, auth_headers):
    response = client.put("/sales/999", json={"total_amount": "100.00"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_sale(client, auth_headers, test_user):
    user_response = client.post("/auth/register", json={
        "username": "salesuser7",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_data = {
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }
    create_response = client.post("/sales", json=sale_data, headers=auth_headers)
    sale_id = create_response.json()["id"]

    response = client.delete(f"/sales/{sale_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/sales/{sale_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_sale(client, auth_headers):
    response = client.delete("/sales/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_sales_without_auth(client):
    response = client.get("/sales")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED