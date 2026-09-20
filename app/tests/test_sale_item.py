import pytest
from fastapi import status
from decimal import Decimal


def test_list_sale_items(client, auth_headers):
    response = client.get("/sale-items", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_sale_item(client, auth_headers):
    # Create a sale first
    user_response = client.post("/auth/register", json={
        "username": "sitemuser1",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    # Create a product
    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU001",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": "10.00"
    }
    response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["sale_id"] == sale_id
    assert data["product_id"] == product_id
    assert data["quantity"] == 2
    assert float(data["unit_price"]) == 10.00
    assert "id" in data


def test_create_sale_item_missing_sale_id(client, auth_headers):
    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU002",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "product_id": product_id,
        "quantity": 2,
        "unit_price": "10.00"
    }
    response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_sale_item_missing_product_id(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "sitemuser2",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "quantity": 2,
        "unit_price": "10.00"
    }
    response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_sale_item_invalid_sale_id(client, auth_headers):
    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU003",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "sale_id": 999,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": "10.00"
    }
    response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Sale" in response.json()["detail"]


def test_create_sale_item_invalid_product_id(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "sitemuser3",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": 999,
        "quantity": 2,
        "unit_price": "10.00"
    }
    response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Product" in response.json()["detail"]


def test_get_sale_item(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "sitemuser4",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU004",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 3,
        "unit_price": "15.00"
    }
    create_response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    sale_item_id = create_response.json()["id"]

    response = client.get(f"/sale-items/{sale_item_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sale_id"] == sale_id
    assert data["product_id"] == product_id
    assert data["quantity"] == 3
    assert float(data["unit_price"]) == 15.00
    assert data["id"] == sale_item_id


def test_get_nonexistent_sale_item(client, auth_headers):
    response = client.get("/sale-items/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Sale item not found"


def test_update_sale_item(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "sitemuser5",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU005",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 1,
        "unit_price": "10.00"
    }
    create_response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    sale_item_id = create_response.json()["id"]

    update_data = {
        "quantity": 5,
        "unit_price": "12.00"
    }
    response = client.put(f"/sale-items/{sale_item_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 5
    assert float(data["unit_price"]) == 12.00


def test_update_sale_item_partial(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "sitemuser6",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU006",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 1,
        "unit_price": "10.00"
    }
    create_response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    sale_item_id = create_response.json()["id"]

    update_data = {"quantity": 10}
    response = client.put(f"/sale-items/{sale_item_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 10
    assert float(data["unit_price"]) == 10.00


def test_update_nonexistent_sale_item(client, auth_headers):
    response = client.put("/sale-items/999", json={"quantity": 5}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_sale_item(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "sitemuser7",
        "password": "password123",
        "role": "Cashier"
    }, headers=auth_headers)
    user_id = user_response.json()["id"]

    sale_response = client.post("/sales", json={
        "total_amount": "100.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id = sale_response.json()["id"]

    prod_response = client.post("/products", json={
        "name": "Test Product",
        "sku": "SKU007",
        "price": "10.00"
    }, headers=auth_headers)
    product_id = prod_response.json()["id"]

    sale_item_data = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 1,
        "unit_price": "10.00"
    }
    create_response = client.post("/sale-items", json=sale_item_data, headers=auth_headers)
    sale_item_id = create_response.json()["id"]

    response = client.delete(f"/sale-items/{sale_item_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/sale-items/{sale_item_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_sale_item(client, auth_headers):
    response = client.delete("/sale-items/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_sale_items_without_auth(client):
    response = client.get("/sale-items")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED