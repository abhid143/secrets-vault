from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Secret
from app.utils.crypto import encrypt_bytes, decrypt_bytes

def create_secret(db: Session, name: str, value: str, owner_id: str) -> Secret:
    encrypted = encrypt_bytes(value)
    secret = Secret(name=name, value=encrypted, owner_id=owner_id)
    db.add(secret)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(secret)
    return secret

def get_secret(db: Session, secret_id: str) -> Secret:
    return db.query(Secret).filter(Secret.id == secret_id).first()

def get_secret_value(db: Session, secret_id: str, owner_id: str):
    s = get_secret(db, secret_id)
    if not s:
        return None
    if s.owner_id != owner_id:
        return None
    return decrypt_bytes(s.value)

def update_secret(db: Session, secret_id: str, owner_id: str, name: str = None, value: str = None):
    s = get_secret(db, secret_id)
    if not s:
        return None
    if s.owner_id != owner_id:
        return "forbidden"
    if name:
        s.name = name
    if value:
        s.value = encrypt_bytes(value)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def delete_secret(db: Session, secret_id: str, owner_id: str):
    s = get_secret(db, secret_id)
    if not s:
        return None
    if s.owner_id != owner_id:
        return "forbidden"
    db.delete(s)
    db.commit()
    return True

def list_secrets_for_owner(db: Session, owner_id: str):
    return db.query(Secret).filter(Secret.owner_id == owner_id).all()
