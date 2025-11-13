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

# Fly (and most PaaS) pass $PORT; default to 8080 for local runs
ENV PORT=8080

# Gunicorn target: your Flask app is `app` inside app.py → app:app
ENV GUNICORN_CMD="app:app"

# Start server with eventlet for Flask-SocketIO
CMD ["sh", "-c", "gunicorn -k eventlet -w 1 --worker-connections 1000 --bind 0.0.0.0:${PORT} ${GUNICORN_CMD}"]
