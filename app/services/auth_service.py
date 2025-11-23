from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.security import create_access_token
from app.db.models import User

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, role: str = "user"):
    """
    Create a user in the DB. Raises IntegrityError if username exists.
    Returns the created user instance.
    """
    user = User(username=username, password_hash=hash_password(password), role=role)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate against DB. Returns dict {username, role} on success, else None.
    """
    u = get_user_by_username(db, username)
    if not u:
        return None
    if not verify_password(password, u.password_hash):
        return None
    return {"username": u.username, "role": u.role}

def create_token_for_user(username: str, role: str):
    return create_access_token(subject=username, role=role)
