import os
import pytest
from cryptography.fernet import Fernet
from app.utils.crypto import encrypt_bytes, decrypt_bytes
from app.core.config import settings

@pytest.fixture(autouse=True)
def set_key(monkeypatch):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("SECRET_ENCRYPTION_KEY", key)
    # re-import settings to pick env change -- hack: directly set
    settings.SECRET_ENCRYPTION_KEY = key
    return key

def test_encrypt_decrypt_roundtrip():
    plaintext = "my secret value"
    blob = encrypt_bytes(plaintext)
    assert isinstance(blob, bytes)
    out = decrypt_bytes(blob)
    assert out == plaintext
