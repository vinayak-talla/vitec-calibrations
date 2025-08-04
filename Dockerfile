# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (required for Cloud SQL Proxy)
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install the Cloud SQL Proxy
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy \
    && chmod +x cloud_sql_proxy

RUN mkdir -p /cloudsql && chmod -R 777 /cloudsql

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput


# Command to start the Cloud SQL Proxy and Gunicorn
CMD ./cloud_sql_proxy -instances=vitec-calibrations-admin:us-central1:vitec-admin-database=unix:/cloudsql/vitec-calibrations-admin:us-central1:vitec-admin-database & \
    sleep 5 && \
    ls -la /cloudsql && \
    gunicorn --bind :$PORT --workers 1 --threads 8 viteccalibrations.wsgi:application
