import uuid
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.db.session import engine, init_db
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_secrets import router as secrets_router
from app.utils.logger import configure_logging
from app.core.rate_limiter import RateLimiter

configure_logging()
logger = logging.getLogger("secrets_vault")

app = FastAPI(title="Secrets Vault")

# CORS (minimal)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory rate limiter (global; for real use replace with Redis)
rate_limiter = RateLimiter(requests=60, per_seconds=60)  # 60 reqs/min per IP

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # correlation id
        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        request.state.request_id = request_id

        # Rate limiting
        client_host = request.client.host if request.client else "unknown"
        allowed, remaining = rate_limiter.allow(client_host)
        if not allowed:
            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

        # proceed
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response

app.add_middleware(RequestContextMiddleware)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(secrets_router, prefix="/secrets", tags=["secrets"])

@app.on_event("startup")
def on_startup():
    logger.info("Starting Secrets Vault service", extra={"service": "secrets_vault"})
    init_db()

@app.get("/healthz")
def health():
    return {"status": "ok"}
