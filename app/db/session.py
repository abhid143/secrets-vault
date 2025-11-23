from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings
from app.db.base import Base
from app.db import models  # noqa: F401

# choose engine based on DATABASE_URL -- if using sqlite, allow check_same_thread
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    # create tables
    Base.metadata.create_all(bind=engine)
