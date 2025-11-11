# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Make Python behave nicely in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (psycopg2 needs libpq-dev; we add gcc & build-essential for safety)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your whole project
COPY . .

# Cloud Run passes $PORT. We'll default to 8080 for local runs.
ENV PORT=8080

# Flexible entrypoint: choose your gunicorn target via env without changing code.
# If you already have wsgi.py exposing "app", leave default as wsgi:app.
# Otherwise set GUNICORN_CMD=app:app or GUNICORN_CMD='app:create_app()' at runtime.
ENV GUNICORN_CMD="wsgi:app"

# Start server
CMD ["sh", "-c", "gunicorn ${GUNICORN_CMD} --bind 0.0.0.0:${PORT} --workers 2 --threads 2 --timeout 120"]
