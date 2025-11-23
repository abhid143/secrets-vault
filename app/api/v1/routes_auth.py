from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest
from app.services import auth_service
from app.db.session import SessionLocal
from sqlalchemy.exc import IntegrityError

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user. Returns access token so client can use it immediately.
    If username already exists, return 400.
    """
    try:
        user = auth_service.create_user(db, username=payload.username, password=payload.password, role=payload.role)
    except IntegrityError:
        # username already exists
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists")
    token = auth_service.create_token_for_user(user.username, user.role)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_service.create_token_for_user(user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer"}
