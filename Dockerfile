FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_ENCRYPTION_KEY=""
ENV DATABASE_URL=postgresql://postgres:Abhi%402283@localhost/secrets_db
ENV JWT_SECRET_KEY=supersecretjwtkey
ENV JWT_ALGORITHM=HS256
ENV JWT_EXP_MINUTES=60

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
