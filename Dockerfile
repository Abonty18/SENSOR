# Use a lightweight base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the desired port
EXPOSE 8000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Start the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
