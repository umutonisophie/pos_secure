import os
import pytest 
from fastapi.testclient import TestClient
import fastapi.testclient as fastapi_testclient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key"

from database import Base, get_db
from main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "hRb4B@example.com",
    }
    
    client.post("/auth/register", json=user_data)
    return user_data

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}



    
    
