# Quantum-Safe Web Application

A comprehensive demonstration web application showcasing post-quantum cryptographic implementations designed to be secure against both classical and quantum computer attacks. Built with Flask, PostgreSQL, and quantum-safe cryptography libraries.

## ⚡ Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd QuantumSafeWebApplications

# Start all services (web app, database, messaging services)
docker-compose up -d

# Access the application
# Web Interface: http://localhost:5000
# With liboqs: Full post-quantum algorithms
# Without liboqs: Simulation mode with RSA fallback
```

**First-time users?** → Start with [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for complete guidance.

## 📋 Key Features

- **🔐 Post-Quantum TLS/SSL**: Kyber768 KEM + Dilithium3 signatures (NIST standardized)
- **📨 Quantum-Safe Messaging**: End-to-end encrypted messaging with ChaCha20-Poly1305
- **💾 Secure Database**: Dual quantum-safe hashing (BLAKE2s-256 + SHA-3-256)
- **🧪 Algorithm Demos**: Interactive demonstrations of 8+ PQC algorithms
- **📊 Real-time Dashboard**: System monitoring, statistics, and algorithm performance
- **🔍 Audit Logging**: Tamper-evident audit trails with BLAKE2s hashing
- **🐳 Docker Deployment**: Production-ready containerized architecture

## 🎯 What Makes This Quantum-Safe?

**The Quantum Threat**: Quantum computers can break RSA, ECDH, and most current encryption within minutes using Shor's algorithm.

**Our Solution**:
- **Kyber768** - Lattice-based key exchange resistant to quantum attacks
- **Dilithium3** - Lattice-based signatures that quantum computers cannot forge
- **BLAKE2s + SHA-3** - Hash functions resistant to Grover's quantum algorithm
- **ChaCha20-Poly1305** - Symmetric encryption (quantum-safe with 256-bit keys)

**Implementation Mode**:
- ✅ **Full PQC Mode**: With liboqs installed, uses real post-quantum algorithms
- ⚠️ **Simulation Mode**: Without liboqs, simulates PQC behavior with RSA-3072 (for demo/testing)

## 🌐 Application URLs

| Interface | URL | Description |
|-----------|-----|-------------|
| **Home** | http://localhost:5000 | Main landing page |
| **Algorithm Demo** | http://localhost:5000/demo | Interactive PQC demonstrations |
| **TLS Demo** | http://localhost:5000/tls | Test quantum-safe TLS |
| **Messaging** | http://localhost:5000/messaging | Secure messaging interface |
| **Dashboard** | http://localhost:5000/dashboard | System stats and monitoring |
| **Documentation** | http://localhost:5000/docs | In-app documentation |
| **API Docs** | http://localhost:5000/api/* | RESTful API endpoints |

## 🔒 Quantum-Safe Algorithms Implemented

### 🔑 Post-Quantum Key Exchange (KEMs)
**Purpose**: Secure key exchange resistant to quantum attacks

| Algorithm | Security Level | Public Key | Ciphertext | Status |
|-----------|---------------|------------|------------|--------|
| **Kyber512** | NIST Level 1 | 800 bytes | 768 bytes | Supported |
| **Kyber768** ⭐ | NIST Level 3 | 1,184 bytes | 1,088 bytes | **Default** |
| **Kyber1024** | NIST Level 5 | 1,568 bytes | 1,568 bytes | Supported |
| NTRU-HPS-2048-509 | Level 1 | 699 bytes | 699 bytes | Supported |
| NTRU-HRSS-701 | Level 3 | 1,138 bytes | 1,138 bytes | Supported |

**Files**: [`app/post_quantum_tls.py:47-56`](app/post_quantum_tls.py#L47-L56)

### ✍️ Post-Quantum Digital Signatures
**Purpose**: Authenticate messages/certificates against quantum forgery

| Algorithm | Security Level | Public Key | Signature | Speed |
|-----------|---------------|------------|-----------|-------|
| DiliSystem Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Browser                             │
│                  (HTTPS with Post-Quantum TLS)                   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                            │
│                   (Ports 80/443, Optional)                       │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Flask Web Application (Port 5000)              │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  run.py    │  │ pq_tls_      │  │  post_quantum_tls.py │   │
│  │ (Routes)   │─▶│ service.py   │─▶│  • Kyber768 KEM      │   │
│  │            │  │              │  │  • Dilithium3 Sigs   │   │
│  └────────────┘  └──────────────┘  │  • ChaCha20 Encrypt  │   │
│                                     └──────────────────────┘   │
│  ┌────────────────────┐  ┌──────────────────────────────────┐ │
│  │ database_service.py│  │         models.py                 │ │
│  │  • Message storage │─▶│  • BLAKE2s + SHA-3 dual hashing  │ │
│  │  • Query handling  │  │  • Integrity verification        │ │
│  └────────────────────┘  └──────────────────────────────────┘ │
└────────────┬──────────────────────┬────────────────────────────┘
             │                      │
             ▼                      ▼
┌──────────────────────┐  ┌───────────────────────────────────────┐
│  PostgreSQL Database │  │   Message Exchange Services           │
│  (Port 5432)         │  │   • Service 1 (Port 6000)             │
│                      │  │   • Service 2 (Port 6001)             │
│  • quantum_safe_     │  │   • Encrypted P2P messaging           │
│    messages table    │  │   • Key exchange protocol             │
│  • message_audit_    │  └───────────────────────────────────────┘
│    logs table        │
│  • Encrypted data    │  ┌───────────────────────────────────────┐
│  • Integrity hashes  │  │   Redis Cache (Port 6379, Optional)   │
└──────────────────────┘  │   • Session storage                   │
                          │   • Key caching                       │
                          └───────────────────────────────────────┘
```
Installation & Setup

### Prerequisites

- **Docker** Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ (Included with Docker Desktop)
- **System Resources**: 
  - 4GB RAM minimum (8GB recommended)
  - 2+ CPU cores
  - 2GB disk space
- **Available Ports**: 5000, 5432, 6000-6001, 6379 (optional)

### Quick Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd QuantumSafeWebApplications

# 2. Build and start all services
docker-compose up -d

# 3. Wait for initialization (30-60 seconds)
docker-compose logs -f quantum-safe-web

# 4. Access the application
open http://localhost:5000
```

### What Gets Started

The `docker-compose up -d` command starts:

| Service | Port | Purpose |
|---------|------|---------|
| **quantum-safe-web** | 5000 | Main Flask application |
| **postgres** | 5432 | PostgreSQL database |
| **message-service-1** | 6000 | Messaging service instance 1 |
| **message-service-2** | 6001 | Messaging service instance 2 |
| **redis** | 6379 | Cache & session storage (optional) |

### Verify Installation

```bash
# Check all services are running
docker-compose ps

# Expected output:
# NAME                     STATUS    PORTS
# quantum-safe-web-app     Up        0.0.0.0:5000->5000/tcp
# quantum-safe-db          Up        5432/tcp
# quantum-message-service-1 Up        0.0.0.0:6000->6000/tcp
# quantum-message-service-2 Up        0.0.0.0:6001->6001/tcp

# Test the application
curl http://localhost:5000/api/tls/supported-algorithms

# Visit in browser
open http://localhost:5000
```

### Development Setup (Without Docker)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install liboqs (optional, for real PQC)
# See: https://github.com/open-quantum-safe/liboqs-python
pip install liboqs

# 3. Set up environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/quantum_safe_db"
export FLASK_ENV=development

# 4. Run the application
cd app
python run.py

# Application available at http://localhost:5000
```
### 🔎 Quantum-Safe Hash Functions
**Purpose**: Data integrity and tamper detection

- **BLAKE2s-256** - Fast, quantum-resistant (primary)
- **SHA-3-256** - NIST standard, Keccak-based (secondary)
- **Dual Hashing Strategy**: Both hashes must match for verification
- **File**: [`app/models.py:94-130`](app/models.py#L94-L130)

## 🏗 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
│   Nginx Proxy   │───▶│  Flask Web App   │───▶│  liboqs Library   │
│  (Port 80/443)  │    │   (Port 5000)    │    │   (PQC Crypto)    │
└─────────────────┘    └──────────────────┘    └───────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
│  SSL/TLS with   │    │   PostgreSQL     │    │  Redis Cache      │
│ Post-Quantum    │    │   Database       │    │   & Sessions      │
│   Certificates  │    │  (Port 5432)     │    │  (Port 6379)      │
└─────────────────┘    └──────────────────┘    └───────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available for containers
- Ports 80, 443, 5000, 5432, 6379 available

### Installation

1. **Clone or download this repository**:
   ```bash
   git clone <repository-url>
   cd QuantumSafeWebApplications
   ```
Guide

### Web Interface

#### 1. Homepage (`/`)
- Overview of quantum-safe cryptography
- Links to all features
- Getting started guide

#### 2. Algorithm Demo (`/demo`)
Interactive demonstrations:
- **KEM (Key Exchange)**: Test Kyber512/768/1024
- **Digital Signatures**: Test Dilithium2/3/5, Falcon
- **Symmetric Encryption**: ChaCha20-Poly1305, AES-256-GCM
- View algorithm performance and key sizes

#### 3. TLS Demo (`/tls`)
- Generate quantum-safe certificates
- View certificate information
- Test handshake protocols
- Compare with classical TLS

#### 4. Messaging Demo (`/messaging`)
- Send encrypted messages between services
- View message history
- Test key exchange
- See BLAKE2s + SHA-3 integrity hashes

#### 5. Dashboard (`/dashboard`)
- Real-time system statistics
- Database message counts
- Algorithm support matrix
- Performance metrics

### API Endpoints Reference

#### TLS/Certificate APIs

```bash
# Get TLS certificate information
curl http://localhost:5000/api/tls/certificate-info

# Get supported algorithms
curl http://localhost:5000/api/tls/supported-algorithms

# Generate new certificate
cur📖 Complete Documentation

This project includes comprehensive documentation for all aspects:

| Document | Purpose | Read If You Want To... |
|----------|---------|------------------------|
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | Navigation hub | Know which doc to read first ⭐ **START HERE** |
| **[CODEBASE_GUIDE.md](CODEBASE_GUIDE.md)** | Complete codebase map | Understand the project structure and find specific files |
| **[ALGORITHM_REFERENCE.md](ALGORITHM_REFERENCE.md)** | Algorithm encyclopedia | Learn about each cryptographic algorithm in detail |
| **[IT_IMPLEMENTATION_GUIDE.md](IT_IMPLEMENTATION_GUIDE.md)** | Practical IT examples | Implement quantum-safe security in real systems |
| **[README.md](README.md)** | Overview (this file) | Get started quickly |
| **[DEPLOYMENT_GUIDE.html](DEPLOYMENT_GUIDE.html)** | Deployment instructions | Deploy to production |

### Quick Links

- **Find an algorithm**: [ALGORITHM_REFERENCE.md](ALGORITHM_REFERENCE.md) - Search for Kyber, Dilithium, etc.
- **Understand a file**: [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) - Module-by-module breakdown
- **Implement in your app**: [IT_IMPLEMENTATION_GUIDE.md](IT_IMPLEMENTATION_GUIDE.md) - Copy-paste examples
- **Navigate efficiently**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Quick lookup guide
curl -X POST http://localhost:5000/api/demo/symmetric \
  -⚙️ Configuration

### Environment Variables

Configure the application via environment variables in `docker-compose.yml` or `.env` file:

```bash
# Flask Application
FLASK_ENV=development              # or 'production'
FLASK_DEBUG=1                      # 0 for production
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://quantum_user:quantum_secure_pass_2024@postgres:5432/quantum_safe_db
POSTGRES_DB=quantum_safe_db
POSTGRES_USER=quantum_user
POSTGRES_PASSWORD=quantum_secure_pass_2024

# Post-Quantum Cryptography
OQS_PROVIDER_PATH=/usr/local/lib/ossl-modules/oqsprovider.so
PQ_TLS_KEM=Kyber768                # Default KEM algorithm
PQ_TLS_SIGNATURE=Dilithium3        # Default signature algorithm

# Messaging Services
SERVICE_ID=service-1               # For message-service-1
SERVICE_PORT=6000                  # Service listen port
PARTNER_SERVICE_URL=http://message-service-2:6001
```

### Algorithm Selection

Default algorithms are configured in [`app/post_quantum_tls.py:68-81`](app/post_quantum_tls.py#L68-L81):

```python
# Change default algorithms
pq_tls = PostQuantumTLS(
    kem_algorithm='Kyber768',      # Options: Kyber512, Kyber768, Kyber1024, NTRU-HPS-2048-509
    sig_algorithm='Dilithium3'     # Options: Dilithium2, Dilithium3, Dilithium5, Falcon-512
)
```
(No Docker)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install liboqs (optional - for real PQC)
pip install liboqs

# 4. Set up PostgreSQL locally
# Install PostgreSQL and create database:
createdb quantum_safe_db

# 5. Configure environment
export DATABASE_URL="postgresql://user:pass@localhost:5432/quantum_safe_db"
export FLASK_ENV=development
export FLASK_DEBUG=1

# 6. Run application
cd app
python run.py

# Access at http://localhost:5000
```

### Development wi& Benchmarks

### System Requirements

| Component | Minimum | Recommended | Production |
|-----------|---------|-------------|------------|
| **CPU** | 2 cores | 4 cores | 8+ cores |
| **RAM** | 4 GB | 8 GB | 16+ GB |
| **Storage** | 2 GB | 10 GB | 50+ GB |
| **Network** | 1 Mbps | 10 Mbps | 100+ Mbps |

### Algorithm Performance (Typical Hardware)

**Intel i7, 3.0 GHz, with liboqs**

| Operation | Algorithm | Time | Throughput |
|-----------|-----------|------|------------|
| **Key Generation** | Kyber768 | ~0.5ms | 2,000 ops/sec |
| **Encapsulation** | Kyber768 | ~0.1ms | 10,000 ops/sec |
| **Decapsulation** | Kyber768 | ~0.15ms | 6,600 ops/sec |
| **Sign** | Dilithium3 | ~0.2ms | 5,000 ops/sec |
| **Verify** | Dilithium3 | ~0.1ms | 10,000 ops/sec |
| **Encrypt** | ChaCha20 | - | ~1 GB/s |
| **Encrypt** | AES-256-GCM (AES-NI) | - | ~5 GB/s |
| **Hash** | BLAKE2s | - | ~500 MB/s |
| **Hash** | SHA-3-256 | - | ~200 MB/s |

### Key/Signature Size Comparison

| Algorithm | Public Key | Private Key | Ciphertext/Sig |
|-----------|------------|-------------|----------------|
| Kyber512 | 800 B | 1,632 B | 768 B |
| Kyber768 | 1,184 B | 2,400 B | 1,088 B |
| Kyber1024 | 1,568 B | 3,168 B | 1,568 B |
| Dilithium2 | 1,312 B | 2,528 B | 2,420 B |
| Dilithium3 | 1,952 B | 4,000 B | 3,293 B |
| Falcon-512 | 897 B | 1,281 B | 690 B |

**Comparison with Classical Crypto**:
- RSA-2048: 256 B public key, 2,048 B private key
- ECDSA P-256: 32 B keys, 64 B signatures
- **PQC keys are 3-10x larger** than classical equivalents
print(f"Public key size: {len(keypair['kem_public_key'])} bytes")

# Test Dilithium signatures
handshake = pq_tls.perform_post_quantum_handshake(
    peer_public_key=keypair['kem_public_key'],
    role='client'
)
print(f"Shared secret: {handshake['shared_secret'][:32]}...")

# Test ChaCha20 encryption
encrypted = pq_tls.encrypt_post_quantum_message(
    message="Te& Production Considerations

### Security Best Practices

✅ **DO**:
- Use hybrid cryptography (classical + post-quantum) for transition period
- Regularly rotate certificates and keys (every 90 days)
- Monitor all cryptographic operations via audit logs
- Use the default algorithms (Kyber768 + Dilithium3) for general use
- Store private keys in HSM or secure key vault in production
- Enable full logging and monitoring
- Keep liboqs and dependencies updated

❌ **DON'T**:
- Use simulation mode in production (requires liboqs installation)
- Store private keys in plain text
- Use the same key pair for all operations
- Expose database directly to the internet
- Disable audit logging
- Use self-signed & Solutions

#### 1. **Port Already in Use**

```bash
# Problem: Port 5000 already in use
Error: bind: address already in use

# Solution: Check what's using the port
# Windows PowerShell:
netstat -ano | findstr :5000
# Linux/Mac:
lsof -i :5000

# Kill the process or change port in docker-compose.yml
ports:
  - "5001:5000"  # Use different host port
```

#### 2. **liboqs Not Available (Simulation Mode)**

```bash
# Problem: "Warning: liboqs not available, using simulation mode"

# Solution: Install liboqs Python bindings
pip install liboqs

# Or rebuild Docker image with liboqs
docker-compose build --no-cache

# Verify installation
python -c "import oqs; print('liboqs version:', oqs.oqs_version())"
```

#### 3. **Database Connection Failed**

```bash
# Problem: psycopg2.OperationalError: could not connect to server

# Solution 1: Wait for PostgreSQL to be ready (30 seconds after start)
docker-compose logs postgres

# Solution 2: Verify database is running
docker-compose ps postgres

# S🎓 Learning Resources

### Understanding Post-Quantum Cryptography

**Start Here**:
1. Read [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Navigation guide
2. Review [ALGORITHM_REFERENCE.md](ALGORITHM_REFERENCE.md) - Algorithm details
3. Try the web demo at http://localhost:5000/demo

**Deep Dive**:
- [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) - Complete code reference
- [IT_IMPLEMENTATION_GUIDE.md](IT_IMPLEMENTATION_GUIDE.md) - Practical examples

**External Resources**:
- [NIST Post-Quantum Cryptography Project](https://csrc.nist.gov/projects/post-quantum-cryptography) - Official standardization
- [Open Quantum Safe](https://openquantumsafe.org/) - liboqs library
- [Kyber Specification](https://pq-crystals.org/kyber/) - Kyber algorithm details
- [Dilithium Specification](https://pq-crystals.org/dilithium/) - Dilithium algorithm details
- [NIST PQ Forum](https://groups.google.com/a/list.nist.gov/g/pqc-forum) - Discussion forum

### Key Concepts

**Quantum Threat**:
- Shor's algorithm breaks RSA, ECDH, DSA
- Grover's algorithm weakens symmetric encryption by half
- "Store now, decrypt later" attacks on encrypted data

**PQC Solution**:
- Lattice-based crypto (Kyber, Dilithium) - hard problems even for quantum computers
- Quantum-safe hashes (BLAKE2s, SHA-3) - resistant to quantum speedup
- Larger keys but still practical (1-3 KB vs. 256 bytes)

## 📄 License & Legal

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Quantum-Safe Web Applications Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

### Third-Party Libraries

This project uses:
- **liboqs** - Open Quantum Safe project (MIT License)
- **Flask** - Web framework (BSD License)
- **PostgreSQL** - Database (PostgreSQL License)
- **PyCryptodome** - Cryptography library (BSD/Public Domain)
- See [requirements.txt](requirements.txt) for complete list

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow the existing code style
4. **Test thoroughly**: Ensure all features work
5. **Update documentation**: Add/update relevant docs
6. **Commit with clear messages**: `git commit -m 'Add Falcon-1024 support'`
7. **Push to your fork**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**: Describe your changes clearly

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add type hints to function signatures
- Write docstrings for all classes and functions
- Update relevant documentation files
- Test with both liboqs and simulation mode
- Ensure backward compatibility

### Areas for Contribution

- 🔐 Additional PQC algorithms (McEliece, BIKE, HQC)
- 🧪 Performance benchmarking suite
- 📱 Mobile app integration examples
- 🌐 Browser extension for quantum-safe browsing
- 📊 Grafana dashboards for monitoring
- 🔍 Security audit and penetration testing
- 📚 Translations and internationalization
- 🎨 UI/UX improvements

## 📞 Support & Contact

- **Documentation**: Start with [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Issues**: Report bugs via GitHub Issues
- **Questions**: Check [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) FAQ section
- **Discussions**: Use GitHub Discussions for general questions

## ⚠️ Important Disclaimers

### Security Notice

**This is a demonstration and educational project.** For production use:

1. ✅ Install liboqs for real post-quantum cryptography
2. ✅ Perform security audit by qualified professionals
3. ✅ Follow your organization's security policies
4. ✅ Use certified cryptographic modules where required
5. ✅ Implement proper key management (HSM, key vault)
6. ✅ Enable comprehensive logging and monitoring
7. ✅ Keep all dependencies updated

### Compliance & Regulations

- Check regulatory requirements for your industry (HIPAA, PCI-DSS, GDPR, etc.)
- Some jurisdictions have restrictions on cryptographic software
- NIST approved only Kyber and Dilithium as of 2024
- Consult legal counsel for compliance questions

### Export Restrictions

This software may be subject to export control laws. Check your local regulations before distributing.

---

## 🚀 Quick Reference

| What You Want | Where To Look |
|---------------|---------------|
| **Get started** | This README (Quick Start section) |
| **Understand algorithms** | [ALGORITHM_REFERENCE.md](ALGORITHM_REFERENCE.md) |
| **Find code** | [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) |
| **Implement in your app** | [IT_IMPLEMENTATION_GUIDE.md](IT_IMPLEMENTATION_GUIDE.md) |
| **Navigate docs** | [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) |
| **Deploy to production** | [DEPLOYMENT_GUIDE.html](DEPLOYMENT_GUIDE.html) |
| **Troubleshoot** | This README (Troubleshooting section) |

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Status**: ✅ Production-ready (with liboqs) / ⚠️ Demo mode (without liboqs)  
**NIST Algorithms**: Kyber768, Dilithium3 (Standardized 2024)

**Built with ❤️ for a Quantum-Safe Future** 🔐🔬
# Solution: Install missing dependencies
pip install -r requirements.txt

# For Docker, rebuild
docker-compose build
```

#### 6. **Certificate Generation Errors**

```bash
# Problem: Certificate validation failed

# Solution: Regenerate certificates
cd app
python -c "from post_quantum_tls import create_post_quantum_certificate_files; \
           create_post_quantum_certificate_files('localhost', '/app/certs')"

# Verify certificates exist
ls -la app/certs/
```

### Debugging Commands

```bash
# View all service logs
docker-compose logs

# Follow logs for specific service (live updates)
docker-compose logs -f quantum-safe-web

# Check service health
curl http://localhost:5000/health

# Enter container for debugging
docker-compose exec quantum-safe-web bash

# Check Python environment inside container
docker-compose exec quantum-safe-web python --version
docker-compose exec quantum-safe-web pip list

# Test database connection
docker-compose exec quantum-safe-web python -c "from database_service import database_service; print('DB connected')"

# Check available algorithms
docker-compose exec quantum-safe-web python -c "from post_quantum_tls import pq_tls; print(pq_tls.get_supported_algorithms())"
```

### Performance Issues

```bash
# Problem: Slow response times

# Check CPU/Memory usage
docker stats

# Problem: High memory usage
# Solution: Increase Docker memory limit in Docker Desktop settings
# or in docker-compose.yml:
services:
  quantum-safe-web:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Getting Help

1. **Check Documentation**:
   - [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Quick navigation
   - [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) - Detailed codebase reference
   - [IT_IMPLEMENTATION_GUIDE.md](IT_IMPLEMENTATION_GUIDE.md) - Implementation examples

2. **Check Logs**:
   ```bash
   # Application logs
   docker-compose logs quantum-safe-web
   
   # Log file (if enabled)
   cat app/logs/app.log
   ```

3. **Test Individual Components**:
   ```bash
   # Test post-quantum TLS
   curl http://localhost:5000/api/tls/supported-algorithms
   
   # Test database
   curl http://localhost:5000/api/database/stats
   
   # Test messaging
   curl http://localhost:5000/api/messaging/status
   # Build with custom Python version
docker build --build-arg PYTHON_VERSION=3.11 -t quantum-safe-web:py311 .

# Build with liboqs for real PQC
docker build --build-arg INSTALL_LIBOQS=true -t quantum-safe-web:liboqs .

# Build for production (optimized)
docker build --build-arg FLASK_ENV=production -t quantum-safe-web:prod .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t quantum-safe-web:multi
```

#### Generate Key Pairs
```bash
curl -X POST http://localhost:5000/api/generate-keys \
  -H "Content-Type: application/json" \
  -d '{"kem_algorithm": "Kyber768", "sig_algorithm": "Dilithium3"}'
```

## 🧪 Supported Algorithms

### Key Encapsulation Mechanisms (KEM)
- **Kyber512** - NIST Level 1 security (~128-bit)
- **Kyber768** - NIST Level 3 security (~192-bit) 
- **Kyber1024** - NIST Level 5 security (~256-bit)
- Additional algorithms available via liboqs

### Digital Signature Schemes
- **Dilithium2** - NIST Level 1 security
- **Dilithium3** - NIST Level 3 security  
- **Dilithium5** - NIST Level 5 security
- **Falcon-512** - NIST Level 1 security
- **Falcon-1024** - NIST Level 5 security
- Additional algorithms available via liboqs

### Hash-Based Signatures
- **SPHINCS+** variants (multiple parameter sets)
- **XMSS** and **LMS** (stateful schemes)

## 🔧 Configuration

### Environment Variables

Create a `.env` file to customize configuration:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-super-secret-key-here

# Database Configuration  
POSTGRES_DB=quantumsafe
POSTGRES_USER=qsafe_user
POSTGRES_PASSWORD=secure-password

# SSL/TLS Configuration
SSL_CERT_PATH=/app/certs/server.crt
SSL_KEY_PATH=/app/certs/server.key

# Security Settings
RATE_LIMIT_API=10
RATE_LIMIT_STATIC=30
```

### Custom Algorithm Configuration

To enable/disable specific algorithms, modify the Python application or use environment variables:

```bash
# Enable only specific KEM algorithms
ENABLED_KEMS="Kyber512,Kyber768,Kyber1024"

# Enable only specific signature algorithms  
ENABLED_SIGS="Dilithium2,Dilithium3,Falcon-512"
```

## 🛠 Development

### Local Development Setup

1. **Install Python dependencies locally**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask app directly**:
   ```bash
   cd app
   python run.py
   ```

3. **Development with hot reload**:
   ```bash
   # Mount local code directory
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
   ```

### Building Custom Images

```bash
# Build with specific liboqs version
docker build --build-arg LIBOQS_VERSION=0.9.0 -t quantum-safe-web:custom .

# Build for production
docker build --build-arg FLASK_ENV=production -t quantum-safe-web:prod .
```

## 📊 Performance Considerations

### Resource Requirements

- **Memory**: 2-4GB RAM recommended
- **CPU**: 2+ cores for optimal performance  
- **Storage**: 1GB+ for containers and data
- **Network**: Standard web application requirements

### Algorithm Performance Comparison

| Algorithm | Key Size | Signature Size | Sign Time | Verify Time |
|-----------|----------|----------------|-----------|-------------|
| Dilithium2 | 1.3KB | 2.4KB | ~0.1ms | ~0.1ms |
| Dilithium3 | 1.9KB | 3.3KB | ~0.2ms | ~0.2ms |
| Falcon-512 | 0.9KB | 0.7KB | ~8ms | ~0.1ms |
| Kyber512 | 0.8KB | 0.8KB | ~0.1ms | ~0.1ms |

*Performance varies by hardware and implementation*

## 🔒 Security Considerations

### Production Deployment

1. **Use proper SSL certificates**: Replace self-signed certificates with CA-issued certificates
2. **Configure firewalls**: Limit access to necessary ports only
3. **Update regularly**: Keep liboqs and dependencies updated
4. **Monitor logs**: Enable comprehensive logging and monitoring
5. **Rate limiting**: Configure appropriate rate limits for your use case

### Known Limitations

- Self-signed certificates for development only
- Some algorithms are research implementations
- Performance may vary significantly between algorithms
- Not all algorithms are NIST-standardized (yet)

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check for port usage
   netstat -tlnp | grep :80
   netstat -tlnp | grep :443
   ```

2. **Container build failures**:
   ```bash
   # Clean build without cache
   docker-compose build --no-cache
   ```

3. **SSL certificate issues**:
   ```bash
   # Regenerate certificates
   docker-compose exec quantum-safe-web bash /etc/config/generate-certs.sh
   ```

4. **Algorithm not found errors**:
   ```bash
   # Check available algorithms
   docker-compose exec quantum-safe-web python -c "import oqs; print(oqs.get_enabled_KEM_mechanisms())"
   ```

### Debugging

Enable debug mode:
```bash
# Set debug environment
export FLASK_DEBUG=1
docker-compose up
```

Check container logs:
```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f quantum-safe-web
```

## 📖 References

- [Open Quantum Safe Project](https://openquantumsafe.org/)
- [liboqs Documentation](https://github.com/open-quantum-safe/liboqs)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Quantum-Safe Security Working Group](https://datatracker.ietf.org/wg/qirg/about/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- Create an issue on GitHub for bug reports
- Check the [FAQ section](#-troubleshooting) for common problems
- Review container logs for debugging information

---

**⚠️ Important Note**: This is a demonstration and educational project. For production use, ensure proper security auditing, use certified implementations, and follow your organization's security guidelines.