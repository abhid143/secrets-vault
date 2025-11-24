Secrets Vault

A small REST API demonstrating secure backend practices:

JWT authentication

Encrypted secret storage

Role-based access

Minimal logging

Rate limiting

Dockerized deployment

🚀 Quickstart (Local Development)

Your project uses config.py for configuration, so .env is optional.

✅ 1. Configure Environment (Required)

Update your values inside:

app/core/config.py


Example:

SECRET_ENCRYPTION_KEY = "your-fernet-key"
DATABASE_URL = "postgresql://postgres:Abhi%402283@localhost/secrets_db"
JWT_SECRET_KEY = "change-this"
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 100000

📝 Optional: .env Support

If you prefer using a .env, you can create one:

SECRET_ENCRYPTION_KEY=<Fernet key>
DATABASE_URL="postgresql://postgres:Abhi%402283@localhost/secrets_db"
JWT_SECRET_KEY=change-this
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=100000


The project loads configuration from config.py by default and only uses .env if provided.

🐳 2. Build & Run with Docker
docker-compose up --build


This will start:

API service

PostgreSQL

Automatic migrations (if enabled)

📡 3. API Endpoints
🔐 Authentication

POST /auth/login
Example body:

{ "username": "alice", "password": "alicepass" }


(Or use bob / bobpass)

Returns a JWT token.

🔏 Secret Management (All require JWT)
➕ Create Secret

POST /secrets

📄 Read Secret Metadata

GET /secrets/{id}
(Owner or admin)

🔑 Read Secret Value

GET /secrets/{id}/value
(Owner only)

✏ Update Secret

PUT /secrets/{id}
(Owner only)

❌ Delete Secret

DELETE /secrets/{id}
(Owner only)

📜 List Secrets by Owner

GET /secrets?owner_id=<id>
(Owner only)

🧪 Tests

To install dependencies:

pip install -r requirements.txt


Run tests:

pytest
