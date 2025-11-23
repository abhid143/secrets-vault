from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class SecretCreate(BaseModel):
    name: constr(min_length=1, max_length=255) # type: ignore
    value: constr(min_length=1, max_length=4096) # type: ignore


class SecretUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)] = None # type: ignore
    value: Optional[constr(min_length=1, max_length=4096)] = None # type: ignore


class SecretOut(BaseModel):
    id: str
    name: str
    owner_id: str
    created_at: datetime
    updated_at: datetime


class SecretValue(BaseModel):
    id: str
    value: str
