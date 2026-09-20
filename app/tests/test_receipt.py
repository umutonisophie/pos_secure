import pytest
from fastapi import status


def test_list_receipts(client, auth_headers):
    response = client.get("/receipts", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_receipt(client, auth_headers):
    # Create a sale first
    user_response = client.post("/auth/register", json={
        "username": "recuser1",
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

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-001"
    }
    response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["sale_id"] == sale_id
    assert data["receipt_number"] == "REC-001"
    assert "id" in data


def test_create_receipt_missing_sale_id(client, auth_headers):
    receipt_data = {
        "receipt_number": "REC-001"
    }
    response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_receipt_missing_receipt_number(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "recuser2",
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

    receipt_data = {
        "sale_id": sale_id
    }
    response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_receipt_invalid_sale_id(client, auth_headers):
    receipt_data = {
        "sale_id": 999,
        "receipt_number": "REC-001"
    }
    response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Sale" in response.json()["detail"]


def test_create_receipt_duplicate_receipt_number(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "recuser3",
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

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-DUPLICATE"
    }
    client.post("/receipts", json=receipt_data, headers=auth_headers)

    # Create another sale
    sale_response2 = client.post("/sales", json={
        "total_amount": "200.00",
        "customer_id": None,
        "user_id": user_id
    }, headers=auth_headers)
    sale_id2 = sale_response2.json()["id"]

    receipt_data2 = {
        "sale_id": sale_id2,
        "receipt_number": "REC-DUPLICATE"
    }
    response = client.post("/receipts", json=receipt_data2, headers=auth_headers)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_receipt(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "recuser4",
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

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-002"
    }
    create_response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    receipt_id = create_response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sale_id"] == sale_id
    assert data["receipt_number"] == "REC-002"
    assert data["id"] == receipt_id


def test_get_nonexistent_receipt(client, auth_headers):
    response = client.get("/receipts/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Receipt not found"


def test_update_receipt(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "recuser5",
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

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-003"
    }
    create_response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    receipt_id = create_response.json()["id"]

    update_data = {
        "receipt_number": "REC-003-UPDATED"
    }
    response = client.put(f"/receipts/{receipt_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["receipt_number"] == "REC-003-UPDATED"


def test_update_nonexistent_receipt(client, auth_headers):
    response = client.put("/receipts/999", json={"receipt_number": "TEST"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_receipt(client, auth_headers):
    user_response = client.post("/auth/register", json={
        "username": "recuser6",
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

    receipt_data = {
        "sale_id": sale_id,
        "receipt_number": "REC-004"
    }
    create_response = client.post("/receipts", json=receipt_data, headers=auth_headers)
    receipt_id = create_response.json()["id"]

    response = client.delete(f"/receipts/{receipt_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/receipts/{receipt_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_receipt(client, auth_headers):
    response = client.delete("/receipts/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_receipts_without_auth(client):
    response = client.get("/receipts")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED