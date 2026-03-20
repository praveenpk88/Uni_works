#!/bin/bash

# Quantum-Safe Web Applications - Quick Start Script
# This script helps you get the quantum-safe web application up and running quickly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker."
        exit 1
    fi
    
    print_success "Prerequisites check passed!"
}

# Check port availability
check_ports() {
    print_status "Checking port availability..."
    
    local ports=(80 443 5000 5432 6379)
    local busy_ports=()
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            busy_ports+=($port)
        fi
    done
    
    if [ ${#busy_ports[@]} -gt 0 ]; then
        print_warning "The following ports are already in use: ${busy_ports[*]}"
        print_warning "You may need to stop other services or modify docker-compose.yml"
        read -p "Continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "All required ports are available!"
    fi
}

# Setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "Created .env file from .env.example"
        else
            print_warning ".env.example not found, creating basic .env file"
            cat > .env << EOF
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
EOF
            print_success "Created basic .env file with secure random secrets"
        fi
    else
        print_success "Environment file .env already exists"
    fi
}

# Build and start containers
build_and_start() {
    print_status "Building and starting containers..."
    
    # Build the application
    print_status "Building quantum-safe web application container..."
    if docker-compose build; then
        print_success "Container built successfully!"
    else
        print_error "Failed to build container"
        exit 1
    fi
    
    # Start services
    print_status "Starting services..."
    if docker-compose up -d; then
        print_success "Services started successfully!"
    else
        print_error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Check if services are healthy
    if docker-compose ps | grep -q "Up (healthy)"; then
        print_success "Services are healthy and ready!"
    else
        print_warning "Some services may still be starting up..."
    fi
}

# Generate SSL certificates
generate_certificates() {
    print_status "Generating SSL certificates..."
    
    if docker-compose exec -T quantum-safe-web bash /etc/config/generate-certs.sh; then
        print_success "SSL certificates generated successfully!"
        
        # Restart nginx to load certificates
        print_status "Restarting nginx to load certificates..."
        docker-compose restart quantum-safe-web
        sleep 10
        print_success "Nginx restarted with SSL certificates!"
    else
        print_error "Failed to generate SSL certificates"
        return 1
    fi
}

# Test the application
test_application() {
    print_status "Testing application..."
    
    # Test health endpoint
    if curl -f http://localhost:5000/health >/dev/null 2>&1; then
        print_success "Health endpoint is responding!"
    else
        print_error "Health endpoint is not responding"
        return 1
    fi
    
    # Test main application
    if curl -f http://localhost >/dev/null 2>&1; then
        print_success "Main application is responding!"
    else
        print_warning "Main application may not be ready yet"
    fi
}

# Show application URLs and info
show_info() {
    print_success "Quantum-Safe Web Application is ready!"
    echo
    echo "=== Application URLs ==="
    echo "Main Application: http://localhost"
    echo "HTTPS (with self-signed cert): https://localhost"  
    echo "Direct Flask App: http://localhost:5000"
    echo "Dashboard: http://localhost/dashboard"
    echo "Interactive Demo: http://localhost/demo"
    echo "Health Check: http://localhost:5000/health"
    echo
    echo "=== Database Access ==="
    echo "PostgreSQL: localhost:5432"
    echo "Database: quantumsafe"
    echo "Username: qsafe_user"
    echo "Redis: localhost:6379"
    echo
    echo "=== Useful Commands ==="
    echo "View logs: docker-compose logs -f"
    echo "Stop services: docker-compose down"
    echo "Restart services: docker-compose restart"
    echo "Execute shell: docker-compose exec quantum-safe-web bash"
    echo
    print_status "Enjoy exploring post-quantum cryptography! 🔐"
}

# Main execution
main() {
    echo "=== Quantum-Safe Web Applications Quick Start ==="
    echo
    
    check_prerequisites
    check_ports
    setup_environment
    build_and_start
    generate_certificates
    
    if test_application; then
        show_info
    else
        print_warning "Application may need more time to start up"
        print_status "Check logs with: docker-compose logs -f"
        show_info
    fi
}

# Handle script arguments
case "${1:-}" in
    "build")
        build_and_start
        ;;
    "certs")
        generate_certificates
        ;;
    "test")
        test_application
        ;;
    "info")
        show_info
        ;;
    "clean")
        print_status "Cleaning up containers and volumes..."
        docker-compose down -v
        docker-compose rm -f
        print_success "Cleanup completed!"
        ;;
    *)
        main
        ;;
esac