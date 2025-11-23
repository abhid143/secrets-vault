# Secrets Vault

Small REST service explaining secure practices: JWT auth, encrypted secrets, limited logging, rate limiting, Dockerized.

## Quickstart (local)

1. create a `.env` file with:
SECRET_ENCRYPTION_KEY=<Fernet key (generate with Python: from cryptography.fernet import Fernet; print(Fernet.generate_key().decode()))>
DATABASE_URL=postgresql://postgres:postgres@db:5432/secrets_db
JWT_SECRET_KEY=change-this
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=60


2. Build & run with Docker:
docker-compose up --build

3. API:
- POST `/auth/login` with `{"username":"alice","password":"alicepass"}` or bob (`bobpass`) to obtain JWT.
- POST `/secrets` create secret (header `Authorization: Bearer <token>`)
- GET `/secrets/{id}` read metadata (owner or admin)
- GET `/secrets/{id}/value` read value (owner only)
- PUT `/secrets/{id}` update (owner only)
- DELETE `/secrets/{id}` delete (owner only)
- GET `/secrets?owner_id=<owner>` list secrets (owner only)

## Tests
Install deps and run:

pip install -r requirements.txt
pytest -q


## Notes & Key Rotation
- Encryption key used by Fernet must be injected via environment (`SECRET_ENCRYPTION_KEY`) — never hard-coded.
- Key rotation: add a key-encryption-key (KEK) or store previous keys in a rotation table. To rotate:
  1. decrypt all records with old key,
  2. re-encrypt with new key,
  3. update env/config to new key,
  4. keep old key until rotation finished & tested.

## Backups & Availability
- Use Postgres backups (pg_dump, point-in-time recovery) and store encrypted backups.
- Run DB in multi-AZ or managed RDS with read replicas for availability and failover.
- Use health checks ( /healthz ) for orchestration.

## Security
- Do not log secret values or full JWTs.
- Validate inputs using Pydantic. Reject unexpected fields.
- Use HTTPS + secure headers in production.
- Replace in-memory rate limiter with Redis for distributed rate-limiting.
