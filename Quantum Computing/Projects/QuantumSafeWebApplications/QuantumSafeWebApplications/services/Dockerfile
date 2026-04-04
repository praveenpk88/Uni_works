# Dockerfile for Quantum-Safe Message Exchange Services
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY message_exchange_service.py /app/

# Create a non-root user
RUN useradd -m -u 1000 serviceuser && chown -R serviceuser:serviceuser /app
USER serviceuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${SERVICE_PORT:-6000}/health || exit 1

# Default command
CMD ["python3", "message_exchange_service.py"]