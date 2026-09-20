import pytest
from fastapi import status


def test_register_user(client):
    user_data = {
        "username": "newuser",
        "password": "password123",
        "role": "Cashier"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "newuser"
    assert data["role"] == "Cashier"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_username(client, test_user):
    user_data = {
        "username": test_user["username"],
        "password": "differentpassword",
        "role": "Cashier"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already exists"


def test_register_missing_username(client):
    user_data = {
        "password": "password123",
        "role": "Cashier"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "password"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_endpoint(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "Cashier"


def test_me_endpoint_no_token(client):
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_endpoint_invalid_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED