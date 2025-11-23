from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_201_CREATED
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.secrets import SecretCreate, SecretOut, SecretValue, SecretUpdate
from app.core.security import get_current_user
from app.db.session import SessionLocal
from app.services import secrets_service
from app.utils.errors import not_found, forbidden, bad_request

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- CREATE SECRET ----------------------
@router.post("", response_model=SecretOut, status_code=HTTP_201_CREATED)
def create_secret(
    payload: SecretCreate,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    owner = current["username"]
    s = secrets_service.create_secret(db, name=payload.name, value=payload.value, owner_id=owner)
    return SecretOut(
        id=s.id,
        name=s.name,
        owner_id=s.owner_id,
        created_at=s.created_at,
        updated_at=s.updated_at
    )


# ---------------------- READ SECRET (metadata only) ----------------------
@router.get("/{secret_id}", response_model=SecretOut)
def read_secret(
    secret_id: str,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    s = secrets_service.get_secret(db, secret_id)
    if not s:
        raise not_found()

    if s.owner_id != current["username"] and current.get("role") != "admin":
        raise forbidden()

    return SecretOut(
        id=s.id,
        name=s.name,
        owner_id=s.owner_id,
        created_at=s.created_at,
        updated_at=s.updated_at
    )


# ---------------------- READ SECRET VALUE ----------------------
@router.get("/{secret_id}/value", response_model=SecretValue)
def read_secret_value(
    secret_id: str,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    owner = current["username"]
    v = secrets_service.get_secret_value(db, secret_id, owner)

    if v is None:
        # Forbidden OR not found
        raise forbidden() if secrets_service.get_secret(db, secret_id) else not_found()

    return SecretValue(id=secret_id, value=v)


# ---------------------- UPDATE SECRET ----------------------
@router.put("/{secret_id}", response_model=SecretOut)
def update_secret(
    secret_id: str,
    payload: SecretUpdate,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    owner = current["username"]

    if payload.name is None and payload.value is None:
        raise bad_request("At least one of name or value must be provided")

    updated = secrets_service.update_secret(
        db,
        secret_id,
        owner,
        name=payload.name,
        value=payload.value
    )

    if updated is None:
        raise not_found()

    if updated == "forbidden":
        raise forbidden()

    return SecretOut(
        id=updated.id,
        name=updated.name,
        owner_id=updated.owner_id,
        created_at=updated.created_at,
        updated_at=updated.updated_at
    )


# ---------------------- DELETE SECRET ----------------------
@router.delete("/{secret_id}")
def delete_secret(
    secret_id: str,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    owner = current["username"]
    res = secrets_service.delete_secret(db, secret_id, owner)

    if res is None:
        raise not_found()

    if res == "forbidden":
        raise forbidden()

    return {"detail": "deleted"}


# ---------------------- LIST SECRETS ----------------------
@router.get("", response_model=list[SecretOut])
def list_secrets(
    owner_id: Optional[str] = Query(None),
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if owner_id is None:
        raise bad_request("owner_id query parameter required")

    if owner_id != current["username"] and current.get("role") != "admin":
        raise forbidden()

    items = secrets_service.list_secrets_for_owner(db, owner_id)

    return [
        SecretOut(
            id=i.id,
            name=i.name,
            owner_id=i.owner_id,
            created_at=i.created_at,
            updated_at=i.updated_at
        )
        for i in items
    ]
