Security & Ops (one page) - ISO27001 controls mapping (high level)

1. Access Control (A.9)
   - JWT-based authentication with expiration.
   - Role separation: "admin" and "user".
   - Owner-only access to secret values.

2. Cryptography (A.10)
   - Symmetric encryption of secret values with Fernet (AES-based).
   - Encryption key injected via environment variable (no hard-code).
   - Key rotation plan described in README.

3. Secure Configuration & Hardening (A.12)
   - Do not run in debug mode inside container.
   - Use ORM / prepared statements (SQLAlchemy) to avoid SQL injection.
   - DB runs on internal Docker network (not exposed).

4. Logging & Monitoring (A.12.4)
   - Structured JSON logs with correlation id.
   - Do not log secret values or full JWTs; only minimal metadata.

5. Operational Resilience (A.17)
   - Health check endpoint `/healthz`.
   - Backup plan: regular pg_dump, encrypted offsite storage; consider PITR on managed DB.
   - Scaling: add replicas and use connection pooling. Use Redis for rate-limiting and caching.

6. Incident Response (A.16)
   - Rotate keys immediately if compromise suspected.
   - Revoke tokens by rotating JWT secret; implement revocation list for production.

7. Change Management & Secure Deployment (A.14)
   - Use CI to build Docker images, sign images, run tests before deployment.
   - Deploy behind load balancer with TLS termination.

Notes:
- For production replace in-memory components (rate limiter, user store) with managed services (Redis, IAM).
