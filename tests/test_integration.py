from fastapi.testclient import TestClient
from app.main import app
from cryptography.fernet import Fernet
from app.core.config import settings

client = TestClient(app)

def setup_module(module):
    # ensure encryption key set for tests
    key = Fernet.generate_key().decode()
    settings.SECRET_ENCRYPTION_KEY = key

    # Register alice and bob
    client.post("/auth/register", json={"username": "alice", "password": "alicepass", "role": "user"})
    client.post("/auth/register", json={"username": "bob", "password": "bobpass", "role": "admin"})

def login(username, password):
    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    return r.json()["access_token"]

def test_create_and_read_secret_as_owner_and_forbidden_for_other():
    alice_token = login("alice", "alicepass")
    bob_token = login("bob", "bobpass")

    # alice creates secret
    r = client.post("/secrets", json={"name": "mykey", "value": "s3cr3t"}, headers={"Authorization": f"Bearer {alice_token}"})
    assert r.status_code == 201
    secret = r.json()
    sid = secret["id"]

    # alice reads metadata
    r2 = client.get(f"/secrets/{sid}", headers={"Authorization": f"Bearer {alice_token}"})
    assert r2.status_code == 200

    # alice reads value
    r3 = client.get(f"/secrets/{sid}/value", headers={"Authorization": f"Bearer {alice_token}"})
    assert r3.status_code == 200
    assert r3.json()["value"] == "s3cr3t"

    # bob tries to read value -> forbidden
    r4 = client.get(f"/secrets/{sid}/value", headers={"Authorization": f"Bearer {bob_token}"})
    assert r4.status_code in (403, 404)
