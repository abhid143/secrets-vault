import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL Database URL
    DATABASE_URL: str = "postgresql://postgres:Abhi%402283@localhost/secrets_db"

    # JWT settings
    JWT_SECRET_KEY: str = "super-secret-key"  # you can replace with your own
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 100000  # long expiry

    # IMPORTANT: This is the correct field name used by crypto.py
    SECRET_ENCRYPTION_KEY: str = "Jx9k1kWmDbN3o1wGhX8QBYxG7sPQ9zlmKsaJ8bCLgBM="  
    # You MUST generate a real Fernet key for production

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60  # seconds

    class Config:
        env_file = ".env"  # not used because you're not using .env

settings = Settings()
