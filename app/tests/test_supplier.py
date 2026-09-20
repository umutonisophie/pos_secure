import pytest
from fastapi import status


def test_list_suppliers(client, auth_headers):
    response = client.get("/suppliers", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "ACME Corp",
        "contact_info": "contact@acme.com"
    }
    response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["company_name"] == "ACME Corp"
    assert data["contact_info"] == "contact@acme.com"
    assert "id" in data


def test_create_supplier_missing_company_name(client, auth_headers):
    supplier_data = {
        "contact_info": "contact@acme.com"
    }
    response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_supplier_missing_contact_info(client, auth_headers):
    supplier_data = {
        "company_name": "ACME Corp"
    }
    response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "Tech Supplies",
        "contact_info": "sales@techsupplies.com"
    }
    create_response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    supplier_id = create_response.json()["id"]

    response = client.get(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_name"] == "Tech Supplies"
    assert data["contact_info"] == "sales@techsupplies.com"
    assert data["id"] == supplier_id


def test_get_nonexistent_supplier(client, auth_headers):
    response = client.get("/suppliers/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Supplier not found"


def test_update_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "Old Corp",
        "contact_info": "old@corp.com"
    }
    create_response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    supplier_id = create_response.json()["id"]

    update_data = {
        "company_name": "New Corp",
        "contact_info": "new@corp.com"
    }
    response = client.put(f"/suppliers/{supplier_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_name"] == "New Corp"
    assert data["contact_info"] == "new@corp.com"


def test_update_supplier_partial(client, auth_headers):
    supplier_data = {
        "company_name": "Partial Update",
        "contact_info": "partial@update.com"
    }
    create_response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    supplier_id = create_response.json()["id"]

    update_data = {"contact_info": "updated@update.com"}
    response = client.put(f"/suppliers/{supplier_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["company_name"] == "Partial Update"
    assert data["contact_info"] == "updated@update.com"


def test_update_nonexistent_supplier(client, auth_headers):
    response = client.put("/suppliers/999", json={"company_name": "Test"}, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_supplier(client, auth_headers):
    supplier_data = {
        "company_name": "To Delete",
        "contact_info": "delete@example.com"
    }
    create_response = client.post("/suppliers", json=supplier_data, headers=auth_headers)
    supplier_id = create_response.json()["id"]

    response = client.delete(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_supplier(client, auth_headers):
    response = client.delete("/suppliers/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_suppliers_without_auth(client):
    response = client.get("/suppliers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED