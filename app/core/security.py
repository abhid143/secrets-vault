from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.config import settings

security = HTTPBearer()

def create_access_token(subject: str, role: str, expires_minutes: Optional[int] = None):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire.timestamp()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(authorization = Depends(security)):
    token = authorization.credentials
    payload = decode_token(token)
    return {"username": payload.get("sub"), "role": payload.get("role")}
