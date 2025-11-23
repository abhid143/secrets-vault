from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from cryptography.fernet import Fernet

client = TestClient(app)

def setup_module(module):
    # ensure encryption key set for tests if used by app
    try:
        key = Fernet.generate_key().decode()
        settings.SECRET_ENCRYPTION_KEY = key
    except Exception:
        pass

def test_register_and_login_success_and_failure():
    # Register a new user
    r = client.post("/auth/register", json={"username": "alice", "password": "alicepass", "role": "user"})
    assert r.status_code in (200, 201)
    data = r.json()
    assert "access_token" in data

    # login success
    r2 = client.post("/auth/login", json={"username": "alice", "password": "alicepass"})
    assert r2.status_code == 200
    d2 = r2.json()
    assert "access_token" in d2

    # login failure (wrong password)
    r3 = client.post("/auth/login", json={"username": "alice", "password": "wrong"})
    assert r3.status_code == 401
