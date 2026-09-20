import pytest
from fastapi import status


def test_list_users(client, auth_headers):
    response = client.get("/users", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_user(client, auth_headers):
    user_data = {
        "username": "newcashier",
        "password": "password123",
        "role": "Cashier"
    }
    response = client.post("/users", json=user_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "newcashier"
    assert data["role"] == "Cashier"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_create_user_missing_username(client, auth_headers):
    user_data = {
        "password": "password123",
        "role": "Cashier"
    }
    response = client.post("/users", json=user_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_missing_password(client, auth_headers):
    user_data = {
        "username": "testuser",
        "role": "Cashier"
    }
    response = client.post("/users", json=user_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_duplicate_username(client, auth_headers):
    user_data = {
        "username": "duplicateuser",
        "password": "password123",
        "role": "Cashier"
    }
    client.post("/users", json=user_data, headers=auth_headers)
    
    user_data2 = {
        "username": "duplicateuser",
        "password": "differentpassword",
        "role": "Cashier"
    }
    response = client.post("/users", json=user_data2, headers=auth_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already exists"


def test_get_user(client, auth_headers):
    user_data = {
        "username": "getuser",
        "password": "password123",
        "role": "Manager"
    }
    create_response = client.post("/users", json=user_data, headers=auth_headers)
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "getuser"
    assert data["role"] == "Manager"
    assert data["id"] == user_id


def test_get_nonexistent_user(client, auth_headers):
    response = client.get("/users/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_update_user(client, auth_headers):
    user_data = {
        "username": "olduser",
        "password": "password123",
        "role": "Cashier"
    }
    create_response = client.post("/users", json=user_data, headers=auth_headers)
    user_id = create_response.json()["id"]

    update_data = {
        "username": "newuser",
        "role": "Manager"
    }
    response = client.put(f"/users/{user_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "newuser"
    assert data["role"] == "Manager"


def test_update_user_password(client, auth_headers):
    user_data = {
        "username": "passuser",
        "password": "oldpassword",
        "role": "Cashier"
    }
    create_response = client.post("/users", json=user_data, headers=auth_headers)
    user_id = create_response.json()["id"]

    update_data = {
        "password": "newpassword"
    }
    response = client.put(f"/users/{user_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "passuser"
    assert data["role"] == "Cashier"
    # Verify we can login with new password
    login_response = client.post("/auth/login", data={
        "username": "passuser",
        "password": "newpassword"
    })
    assert login_response.status_code == status.HTTP_200_OK


def test_update_user_duplicate_username(client, auth_headers):
    user_data1 = {
        "username": "user1",
        "password": "password123",
        "role": "Cashier"
    }
    create_response1 = client.post("/users", json=user_data1, headers=auth_headers)
    user_id1 = create_response1.json()["id"]

    user_data2 = {
        "username": "user2",
        "password": "password123",
        "role": "Cashier"
    }
    create_response2 = client.post("/users", json=user_data2, headers=auth_headers)
    user_id2 = create_response2.json()["id"]

    # Try to update user2 with user1's username
    update_data = {"username": "user1"}
    response = client.put(f"/users/{user_id2}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already exists"


def test_update_nonexistent_user(client, auth_headers):
    response = client.put("/users/999", json={"username": "test"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(client, auth_headers):
    user_data = {
        "username": "todelete",
        "password": "password123",
        "role": "Cashier"
    }
    create_response = client.post("/users", json=user_data, headers=auth_headers)
    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_user(client, auth_headers):
    response = client.delete("/users/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_users_without_auth(client):
    response = client.get("/users")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED