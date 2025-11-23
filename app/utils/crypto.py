import base64
from cryptography.fernet import Fernet
from app.core.config import settings
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

def _get_fernet():
    key = settings.SECRET_ENCRYPTION_KEY
    if not key:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Encryption key is not configured")
    # If user provides raw 32 bytes, ensure base64 urlsafe; accept already-base64 too
    try:
        # if key length looks like raw 32 bytes, base64-encode
        b = key.encode()
        # try to interpret as base64
        Fernet(b)
        return Fernet(b)
    except Exception:
        # try to create from raw key
        try:
            k = base64.urlsafe_b64encode(b)
            return Fernet(k)
        except Exception:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid encryption key format")

def encrypt_bytes(plaintext: str) -> bytes:
    f = _get_fernet()
    return f.encrypt(plaintext.encode())

def decrypt_bytes(blob: bytes) -> str:
    f = _get_fernet()
    return f.decrypt(blob).decode()
