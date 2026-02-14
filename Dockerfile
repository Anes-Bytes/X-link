# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Remove unnecessary files
RUN rm -rf venv .idea db.sqlite3

# Run entrypoint script
COPY ./entrypoint.sh /app/
RUN sed -i 's/\r$//' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
