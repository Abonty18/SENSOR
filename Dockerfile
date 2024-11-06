# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
