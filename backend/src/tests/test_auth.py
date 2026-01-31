import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_signup_and_login():
    # Signup
    response = client.post("/signup/auth/signup", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "id" in data

    # Login
    response = client.post("/signup/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
