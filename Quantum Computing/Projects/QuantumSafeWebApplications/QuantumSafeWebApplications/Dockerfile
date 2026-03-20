# Quantum-Safe Web Applications Docker Container
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libffi-dev \
    libssl-dev \
    nginx \
    pkg-config \
    python3 \
    python3-dev \
    python3-pip \
    supervisor \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Install Python packages first (this layer will be cached if requirements don't change)
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ /app/
COPY config/ /etc/

# Set up nginx configuration
COPY config/nginx.conf /etc/nginx/sites-available/quantum-safe
RUN ln -s /etc/nginx/sites-available/quantum-safe /etc/nginx/sites-enabled/ && \
    rm /etc/nginx/sites-enabled/default

# Create directories for certificates and logs
RUN mkdir -p /app/certs /app/logs /var/log/supervisor

# Copy supervisor configuration
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 443 5000

# Set proper permissions
RUN chown -R www-data:www-data /app && \
    chmod +x /app/run.py

# Update library cache
RUN ldconfig

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start supervisor to manage services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]