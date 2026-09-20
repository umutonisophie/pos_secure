import pytest
from fastapi import status
from decimal import Decimal


def test_list_products(client, auth_headers):
    response = client.get("/products", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_product(client, auth_headers):
    product_data = {
        "name": "Coca Cola",
        "sku": "SKU123",
        "price": 10.99,
        "cost": 5.00,
        "category_id": None,
        "supplier_id": None,
        "is_active": True
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Coca Cola"
    assert data["sku"] == "SKU123"
    assert float(data["price"]) == 10.99
    assert float(data["cost"]) == 5.00
    assert data["is_active"] is True
    assert "id" in data


def test_create_product_with_category_and_supplier(client, auth_headers):
    # Create category and supplier first
    cat_response = client.post("/categories", json={"name": "Drinks"}, headers=auth_headers)
    category_id = cat_response.json()["id"]
    
    sup_response = client.post("/suppliers", json={"company_name": "Coke Inc", "contact_info": "coke@inc.com"}, headers=auth_headers)
    supplier_id = sup_response.json()["id"]

    product_data = {
        "name": "Sprite",
        "sku": "SKU456",
        "price": 9.99,
        "cost": 4.50,
        "category_id": category_id,
        "supplier_id": supplier_id,
        "is_active": True
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Sprite"
    assert data["category_id"] == category_id
    assert data["supplier_id"] == supplier_id


def test_create_product_missing_name(client, auth_headers):
    product_data = {
        "sku": "SKU123",
        "price": 10.99
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_missing_sku(client, auth_headers):
    product_data = {
        "name": "Product",
        "price": 10.99
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_missing_price(client, auth_headers):
    product_data = {
        "name": "Product",
        "sku": "SKU123"
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_duplicate_sku(client, auth_headers):
    product_data = {
        "name": "Product 1",
        "sku": "DUPLICATE",
        "price": 10.99
    }
    client.post("/products", json=product_data, headers=auth_headers)
    
    product_data2 = {
        "name": "Product 2",
        "sku": "DUPLICATE",
        "price": 15.99
    }
    response = client.post("/products", json=product_data2, headers=auth_headers)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_product_invalid_category_id(client, auth_headers):
    product_data = {
        "name": "Product",
        "sku": "SKU123",
        "price": 10.99,
        "category_id": 999
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Category" in response.json()["detail"]


def test_create_product_invalid_supplier_id(client, auth_headers):
    product_data = {
        "name": "Product",
        "sku": "SKU123",
        "price": 10.99,
        "supplier_id": 999
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Supplier" in response.json()["detail"]


def test_get_product(client, auth_headers):
    product_data = {
        "name": "Fanta",
        "sku": "SKU789",
        "price": 8.99
    }
    create_response = client.post("/products", json=product_data, headers=auth_headers)
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Fanta"
    assert data["sku"] == "SKU789"
    assert float(data["price"]) == 8.99
    assert data["id"] == product_id


def test_get_nonexistent_product(client, auth_headers):
    response = client.get("/products/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found"


def test_update_product(client, auth_headers):
    product_data = {
        "name": "Old Product",
        "sku": "OLD123",
        "price": 5.00
    }
    create_response = client.post("/products", json=product_data, headers=auth_headers)
    product_id = create_response.json()["id"]

    update_data = {
        "name": "New Product",
        "sku": "NEW123",
        "price": 6.00,
        "cost": 3.00,
        "is_active": False
    }
    response = client.put(f"/products/{product_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Product"
    assert data["sku"] == "NEW123"
    assert float(data["price"]) == 6.00
    assert float(data["cost"]) == 3.00
    assert data["is_active"] is False


def test_update_product_partial(client, auth_headers):
    product_data = {
        "name": "Partial Product",
        "sku": "PART123",
        "price": 10.00
    }
    create_response = client.post("/products", json=product_data, headers=auth_headers)
    product_id = create_response.json()["id"]

    update_data = {"price": 15.00}
    response = client.put(f"/products/{product_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Partial Product"
    assert float(data["price"]) == 15.00


def test_update_product_with_category(client, auth_headers):
    cat_response = client.post("/categories", json={"name": "Test Category"}, headers=auth_headers)
    category_id = cat_response.json()["id"]

    product_data = {
        "name": "Product",
        "sku": "SKU123",
        "price": 10.99
    }
    create_response = client.post("/products", json=product_data, headers=auth_headers)
    product_id = create_response.json()["id"]

    update_data = {"category_id": category_id}
    response = client.put(f"/products/{product_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["category_id"] == category_id


def test_update_nonexistent_product(client, auth_headers):
    response = client.put("/products/999", json={"name": "Test"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product(client, auth_headers):
    product_data = {
        "name": "To Delete",
        "sku": "DEL123",
        "price": 10.99
    }
    create_response = client.post("/products", json=product_data, headers=auth_headers)
    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_product(client, auth_headers):
    response = client.delete("/products/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_products_without_credentials_returns_401(client):
    response = client.get("/products")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED