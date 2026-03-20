#!/bin/bash

# Certificate generation script for quantum-safe web applications
# This script generates SSL certificates for development purposes

CERTS_DIR="/app/certs"
COUNTRY="AU"
STATE="Victoria"
CITY="Melbourne"
ORG="RMIT University"
UNIT="Quantum Summer School"
COMMON_NAME="quantum-safe-web.local"

# Create certs directory if it doesn't exist
mkdir -p "$CERTS_DIR"

echo "Generating quantum-safe certificates..."

# Generate private key
openssl genrsa -out "$CERTS_DIR/server.key" 4096

# Generate certificate signing request
openssl req -new -key "$CERTS_DIR/server.key" -out "$CERTS_DIR/server.csr" -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/OU=$UNIT/CN=$COMMON_NAME"

# Generate self-signed certificate
openssl x509 -req -days 365 -in "$CERTS_DIR/server.csr" -signkey "$CERTS_DIR/server.key" -out "$CERTS_DIR/server.crt"

# Generate Diffie-Hellman parameters
openssl dhparam -out "$CERTS_DIR/dhparam.pem" 2048

# Set appropriate permissions
chmod 600 "$CERTS_DIR/server.key"
chmod 644 "$CERTS_DIR/server.crt"
chmod 644 "$CERTS_DIR/dhparam.pem"

# Clean up CSR
rm -f "$CERTS_DIR/server.csr"

echo "Certificates generated successfully in $CERTS_DIR"
echo "Note: These are self-signed certificates for development use only."
echo "For production, use certificates from a trusted CA with post-quantum support."