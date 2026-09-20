import pytest
from fastapi import status
from decimal import Decimal


def test_list_payments(client, auth_headers):
    response = client.get("/payments", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_payment(client, auth_headers):
    # Create a sale first
    user_response = client.post("/auth/register", json={
        "username": "payuser1",
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

    payment_data = {
        "sale_id": sale_id,
        "amount": "50.00",
        "payment_type": "Cash"
    }
    response = client.post("/payments", json=payment_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["sale_id"] == sale_id
    assert float(data["amount"]) == 50.00
    assert data["payment_type"] == "Cash"
    assert "id" in data


def test_create_payment_missing_sale_id(client, auth_headers):
    payment_data = {
        "amount": "50.00",
        "payment_type": "Cash"
    }
    response = client.post("/payments", json=payment_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_payment_missing_amount(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "payuser2",
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

    payment_data = {
        "sale_id": sale_id,
        "payment_type": "Cash"
    }
    response = client.post("/payments", json=payment_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_payment_missing_payment_type(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "payuser3",
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

    payment_data = {
        "sale_id": sale_id,
        "amount": "50.00"
    }
    response = client.post("/payments", json=payment_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_payment_invalid_sale_id(client, auth_headers):
    payment_data = {
        "sale_id": 999,
        "amount": "50.00",
        "payment_type": "Cash"
    }
    response = client.post("/payments", json=payment_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Sale" in response.json()["detail"]


def test_get_payment(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "payuser4",
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

    payment_data = {
        "sale_id": sale_id,
        "amount": "75.00",
        "payment_type": "Card"
    }
    create_response = client.post("/payments", json=payment_data, headers=auth_headers)
    payment_id = create_response.json()["id"]

    response = client.get(f"/payments/{payment_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sale_id"] == sale_id
    assert float(data["amount"]) == 75.00
    assert data["payment_type"] == "Card"
    assert data["id"] == payment_id


def test_get_nonexistent_payment(client, auth_headers):
    response = client.get("/payments/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Payment not found"


def test_update_payment(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "payuser5",
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

    payment_data = {
        "sale_id": sale_id,
        "amount": "25.00",
        "payment_type": "Cash"
    }
    create_response = client.post("/payments", json=payment_data, headers=auth_headers)
    payment_id = create_response.json()["id"]

    update_data = {
        "amount": "30.00",
        "payment_type": "Card"
    }
    response = client.put(f"/payments/{payment_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert float(data["amount"]) == 30.00
    assert data["payment_type"] == "Card"


def test_update_payment_partial(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "payuser6",
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

    payment_data = {
        "sale_id": sale_id,
        "amount": "25.00",
        "payment_type": "Cash"
    }
    create_response = client.post("/payments", json=payment_data, headers=auth_headers)
    payment_id = create_response.json()["id"]

    update_data = {"payment_type": "Mobile"}
    response = client.put(f"/payments/{payment_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert float(data["amount"]) == 25.00
    assert data["payment_type"] == "Mobile"


def test_update_nonexistent_payment(client, auth_headers):
    response = client.put("/payments/999", json={"amount": "50.00"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_payment(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "payuser7",
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

    payment_data = {
        "sale_id": sale_id,
        "amount": "25.00",
        "payment_type": "Cash"
    }
    create_response = client.post("/payments", json=payment_data, headers=auth_headers)
    payment_id = create_response.json()["id"]

    response = client.delete(f"/payments/{payment_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/payments/{payment_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_payment(client, auth_headers):
    response = client.delete("/payments/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_payments_without_auth(client):
    response = client.get("/payments")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED