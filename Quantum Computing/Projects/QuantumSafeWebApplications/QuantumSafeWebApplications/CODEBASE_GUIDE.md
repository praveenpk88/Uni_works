# Quantum-Safe Web Applications - Complete Codebase Guide

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure & File Locations](#directory-structure--file-locations)
3. [Cryptographic Algorithms Implemented](#cryptographic-algorithms-implemented)
4. [How to Use These Algorithms in IT](#how-to-use-these-algorithms-in-it)
5. [Module-by-Module Breakdown](#module-by-module-breakdown)
6. [API Endpoints Reference](#api-endpoints-reference)
7. [Database Schema](#database-schema)
8. [Deployment & Configuration](#deployment--configuration)

---

## 🎯 Project Overview

This is a **Quantum-Safe Web Application** that demonstrates post-quantum cryptography (PQC) implementations designed to protect against both classical and quantum computer attacks. The application showcases:

- **Post-Quantum TLS/SSL** connections
- **Quantum-resistant message encryption**
- **Secure database storage with quantum-safe hashing**
- **Interactive algorithm demonstrations**

**Current Status**: Hybrid mode with simulation fallback when liboqs is not available.

---

## 📁 Directory Structure & File Locations

```
QuantumSafeWebApplications/
│
├── app/                              # Main Flask application
│   ├── run.py                        # 🔹 Main Flask app & API routes
│   ├── post_quantum_tls.py          # 🔒 Core post-quantum TLS implementation
│   ├── pq_tls_service.py            # 🔒 Flask TLS service integration
│   ├── database_service.py          # 💾 Database operations & message storage
│   ├── models.py                    # 💾 SQLAlchemy database models
│   ├── templates/                   # Web UI templates
│   │   ├── index.html               # Homepage
│   │   ├── demo.html                # Algorithm demonstrations
│   │   ├── tls.html                 # TLS demonstrations
│   │   ├── messaging.html           # Messaging interface
│   │   ├── dashboard.html           # System dashboard
│   │   └── documentation.html       # Documentation page
│   ├── certs/                       # TLS certificates storage
│   └── logs/                        # Application logs
│
├── services/                        # Microservices
│   ├── message_exchange_service.py # 📨 Quantum-safe messaging service
│   ├── Dockerfile                   # Service container config
│   └── requirements.txt             # Service dependencies
│
├── config/                          # Configuration files
│   ├── nginx.conf                   # Nginx reverse proxy config
│   ├── supervisord.conf             # Process supervisor config
│   └── generate-certs.sh           # Certificate generation script
│
├── certs/                           # Root certificates directory
├── logs/                            # Application logs
│
├── docker-compose.yml               # 🐳 Multi-container orchestration
├── Dockerfile                       # 🐳 Main app container
├── requirements.txt                 # Python dependencies
├── init-db.sql                      # Database initialization
├── README.md                        # Project README
└── DEPLOYMENT_GUIDE.html            # Deployment instructions
```

---

## 🔐 Cryptographic Algorithms Implemented

### 1. **Post-Quantum Key Exchange Mechanisms (KEMs)**

**Location**: [`app/post_quantum_tls.py`](app/post_quantum_tls.py) - Lines 47-56

**Algorithms Supported**:
- **Kyber512** - NIST Level 1 (128-bit security)
- **Kyber768** ⭐ (Default) - NIST Level 3 (192-bit security)
- **Kyber1024** - NIST Level 5 (256-bit security)
- **NTRU-HPS-2048-509** - Lattice-based alternative
- **NTRU-HRSS-701** - Higher security NTRU variant
- **Classic-McEliece-348864** - Code-based cryptography
- **BIKE-L1** - Code-based KEM
- **HQC-128** - Code-based KEM

**What They Do**: Exchange cryptographic keys securely over insecure networks, resistant to quantum attacks.

**Implementation Details**:
- Uses `liboqs` library when available (real PQC)
- Falls back to RSA-3072 simulation when liboqs is unavailable
- Key generation: `generate_post_quantum_keypair()` method

---

### 2. **Post-Quantum Digital Signatures**

**Location**: [`app/post_quantum_tls.py`](app/post_quantum_tls.py) - Lines 58-66

**Algorithms Supported**:
- **Dilithium2** - NIST standardized (Level 2)
- **Dilithium3** ⭐ (Default) - NIST standardized (Level 3)
- **Dilithium5** - NIST standardized (Level 5)
- **Falcon-512** - Lattice-based compact signatures
- **Falcon-1024** - Higher security Falcon variant
- **SPHINCS+-SHA256-128s-robust** - Hash-based signatures
- **SPHINCS+-SHAKE256-128s-robust** - Hash-based with SHAKE

**What They Do**: Digitally sign messages and certificates to prove authenticity, resistant to quantum forgery.

**Implementation Details**:
- Signature generation and verification
- Certificate signing using post-quantum algorithms
- Falls back to RSA-PSS in simulation mode

---

### 3. **Symmetric Encryption Algorithms**

**Location**: [`app/post_quantum_tls.py`](app/post_quantum_tls.py) - Lines 324-390

**Algorithms Supported**:
- **ChaCha20-Poly1305** ⭐ (Preferred)
  - Stream cipher with authenticated encryption
  - 256-bit keys, 96-bit nonces
  - AEAD (Authenticated Encryption with Associated Data)
  
- **AES-256-GCM**
  - Block cipher in Galois/Counter Mode
  - 256-bit keys, 128-bit authentication tags
  - NIST approved, hardware-accelerated

**What They Do**: Encrypt actual message content after key exchange is complete.

**Implementation Details**:
- Key derivation using BLAKE2s-256
- Authenticated encryption (prevents tampering)
- Used in `encrypt_post_quantum_message()` method

---

### 4. **Quantum-Safe Hash Functions**

**Location**: [`app/models.py`](app/models.py) - Lines 94-130

**Algorithms Supported**:
- **BLAKE2s-256** - Quantum-resistant, faster than SHA-3
  - 256-bit output
  - Resistant to length extension attacks
  
- **SHA-3-256** (Keccak)
  - NIST standardized quantum-resistant hash
  - 256-bit output
  - Sponge construction

**What They Do**: Create message digests for integrity verification and tamper detection.

**Implementation Details**:
- Dual hashing for defense in depth
- Used in database models for message integrity
- Content hashing for deduplication
- Audit trail hashing with BLAKE2s

---

### 5. **Key Derivation Functions (KDF)**

**Location**: [`app/post_quantum_tls.py`](app/post_quantum_tls.py) - Lines 324-338

**Algorithms Supported**:
- **BLAKE2s-256 KDF**
  - Derives encryption keys from shared secrets
  - Salt: "POST_QUANTUM_TLS_v1.0"
  
- **HKDF-SHA3-256**
  - HMAC-based key derivation (available)

**What They Do**: Transform shared secrets into usable encryption keys.

---

### 6. **Classical Cryptography (Fallback)**

**Location**: [`app/post_quantum_tls.py`](app/post_quantum_tls.py) - Lines 99-107

**Algorithms**:
- **RSA-3072** - Key exchange simulation
- **RSA-PSS** - Signature simulation
- **RSA-OAEP** - Encryption padding

**Purpose**: Simulate post-quantum behavior when liboqs is unavailable.

---

## 💼 How to Use These Algorithms in IT

### **A. Secure Web Communications (TLS/SSL Replacement)**

**Use Case**: Replace traditional TLS 1.2/1.3 with quantum-safe TLS

**Location**: [`app/pq_tls_service.py`](app/pq_tls_service.py)

**How to Implement**:
```python
from pq_tls_service import PostQuantumTLSService

# Initialize post-quantum TLS for your Flask app
tls_service = PostQuantumTLSService(app)

# Certificates are automatically generated with:
# - Kyber768 for key exchange
# - Dilithium3 for signatures

# Access at: https://your-domain.com with quantum-safe TLS
```

**IT Applications**:
- **Banking & Finance**: Protect transaction channels from future quantum attacks
- **Healthcare**: Secure patient data transmission (HIPAA compliance)
- **Government**: Classified communications
- **E-commerce**: Payment processing security
- **VPN Services**: Quantum-safe virtual private networks

---

### **B. Secure Messaging Systems**

**Use Case**: End-to-end encrypted messaging resistant to quantum decryption

**Location**: [`services/message_exchange_service.py`](services/message_exchange_service.py)

**How to Implement**:
```python
# Service 1 sends encrypted message to Service 2
POST /api/messaging/send
{
    "message": "Sensitive information",
    "sender_service": "service-1"
}

# Message is encrypted with:
# 1. AES-256-CBC for message content
# 2. RSA-OAEP for key encapsulation (simulating Kyber)
# 3. RSA-PSS for digital signatures (simulating Dilithium)
```

**IT Applications**:
- **Corporate Communications**: Inter-department secure messaging
- **Military/Defense**: Command and control communications
- **Healthcare**: Doctor-patient secure messaging
- **Legal**: Attorney-client privileged communications
- **IoT**: Secure device-to-device communication

---

### **C. Database Security & Integrity Verification**

**Use Case**: Store data with quantum-safe hashing for tamper detection

**Location**: [`app/models.py`](app/models.py) & [`app/database_service.py`](app/database_service.py)

**How to Implement**:
```python
# Automatic quantum-safe hashing when saving messages
from database_service import database_service

message = database_service.save_message(
    sender_service_id="user123",
    receiver_service_id="user456",
    encrypted_data=encrypted_data,
    original_message="Original text"
)

# Stored with:
# - BLAKE2s-256 hash
# - SHA-3-256 hash
# - Content hash for deduplication
```

**IT Applications**:
- **Blockchain/DLT**: Quantum-resistant blockchain implementations
- **Medical Records**: Tamper-evident health records
- **Financial Auditing**: Immutable audit trails
- **Supply Chain**: Track and verify product authenticity
- **Digital Evidence**: Law enforcement evidence integrity

---

### **D. Certificate Management**

**Use Case**: Generate and manage post-quantum X.509 certificates

**Location**: [`app/post_quantum_tls.py`](app/post_quantum_tls.py) - Lines 151-238

**How to Implement**:
```python
from post_quantum_tls import create_post_quantum_certificate_files

# Generate post-quantum certificate
cert_file, key_file = create_post_quantum_certificate_files(
    domain="secure.example.com",
    output_dir="/certs"
)

# Certificate includes:
# - Post-quantum public key
# - Signed with post-quantum signature algorithm
# - Standard X.509 format (compatible with existing tools)
```

**IT Applications**:
- **PKI Systems**: Quantum-safe public key infrastructure
- **Code Signing**: Sign software with quantum-resistant signatures
- **Device Authentication**: IoT device certificates
- **Email Security**: S/MIME email encryption
- **Document Signing**: PDF and document digital signatures

---

### **E. API Security & Authentication**

**Use Case**: Secure REST APIs with quantum-safe authentication

**Location**: [`app/run.py`](app/run.py) - API Routes

**Available Endpoints**:

1. **TLS Certificate Management**:
   ```
   GET /api/tls/certificate-info
   POST /api/tls/generate-certificate
   GET /api/tls/supported-algorithms
   ```

2. **Messaging APIs**:
   ```
   GET /api/messaging/status
   POST /api/messaging/initiate-key-exchange
   POST /api/messaging/send
   GET /api/messaging/history/<service_id>
   ```

3. **Algorithm Demonstrations**:
   ```
   POST /api/demo/kem
   POST /api/demo/signature
   POST /api/demo/symmetric
   ```

**IT Applications**:
- **Microservices**: Secure service-to-service communication
- **API Gateways**: Quantum-safe API authentication
- **Mobile Apps**: Secure mobile-backend communication
- **Third-party Integrations**: Partner API security

---

### **F. Real-World Implementation Examples**

#### **Example 1: Secure File Transfer**
```python
# 1. Generate post-quantum key pair
keypair = pq_tls.generate_post_quantum_keypair()

# 2. Perform key exchange with recipient
handshake = pq_tls.perform_post_quantum_handshake(
    peer_public_key=recipient_public_key,
    role='client'
)

# 3. Encrypt file with shared secret
encrypted_file = pq_tls.encrypt_post_quantum_message(
    message=file_contents,
    shared_secret=handshake['shared_secret'],
    algorithm='ChaCha20-Poly1305'
)

# 4. Send encrypted file over network
# 5. Recipient decrypts with their copy of shared secret
```

**Use Cases**: 
- Cloud storage encryption
- Secure email attachments
- File sharing services

---

#### **Example 2: Secure Session Management**
```python
# Web application session with quantum-safe protection

# 1. User logs in
# 2. Generate quantum-safe session token
session_id = pq_tls.generate_session_id()

# 3. Encrypt session data with ChaCha20-Poly1305
encrypted_session = pq_tls.encrypt_post_quantum_message(
    message=json.dumps(session_data),
    shared_secret=server_master_key,
    algorithm='ChaCha20-Poly1305'
)

# 4. Store in Redis/database with BLAKE2s hash
# 5. Verify integrity on each request
```

**Use Cases**:
- Web application sessions
- Single Sign-On (SSO) systems
- Token-based authentication

---

#### **Example 3: Audit Logging System**
```python
# Quantum-safe audit trail for compliance

# 1. Create audit log entry
audit_log = MessageAuditLog(
    message_id=123,
    operation='update',
    context={'user': 'admin', 'action': 'modify_record'}
)

# 2. Automatically generates BLAKE2s audit hash
# 3. Stored in database with tamper detection
# 4. Verify integrity at any time:

if audit_log.audit_hash == recalculated_hash:
    print("Audit trail intact - no tampering detected")
```

**Use Cases**:
- SOC 2 compliance
- GDPR audit requirements
- Financial regulations (SOX, PCI-DSS)
- Healthcare compliance (HIPAA)

---

## 📦 Module-by-Module Breakdown

### **1. `app/post_quantum_tls.py`** (488 lines)

**Purpose**: Core post-quantum cryptography implementation

**Key Classes**:
- `PostQuantumTLS` - Main PQC class

**Key Methods**:
| Method | Purpose | Lines |
|--------|---------|-------|
| `__init__()` | Initialize with KEM and signature algorithms | 68-81 |
| `generate_post_quantum_keypair()` | Generate PQ key pairs | 109-146 |
| `generate_post_quantum_certificate()` | Create X.509 certificates | 148-238 |
| `perform_post_quantum_handshake()` | TLS handshake simulation | 240-293 |
| `encrypt_post_quantum_message()` | Encrypt with ChaCha20/AES | 295-352 |
| `decrypt_post_quantum_message()` | Decrypt messages | 354-393 |
| `get_supported_algorithms()` | List available algorithms | 395-404 |

**Dependencies**:
- `oqs` (liboqs Python bindings) - Optional
- `cryptography` - Certificate generation
- `pycryptodome` - ChaCha20, AES, hashing

---

### **2. `app/pq_tls_service.py`** (352 lines)

**Purpose**: Flask integration for post-quantum TLS

**Key Classes**:
- `PostQuantumTLSService` - Flask TLS service

**Key Methods**:
| Method | Purpose |
|--------|---------|
| `init_app()` | Initialize with Flask |
| `_setup_certificates()` | Generate/load certificates |
| `_register_tls_routes()` | Register API endpoints |

**API Routes Registered**:
- `/api/tls/certificate-info` - Get certificate details
- `/api/tls/generate-certificate` - Generate new certificate
- `/api/tls/supported-algorithms` - List algorithms

---

### **3. `app/database_service.py`** (261 lines)

**Purpose**: Database operations with quantum-safe hashing

**Key Classes**:
- `DatabaseService` - Database operations manager

**Key Methods**:
| Method | Purpose |
|--------|---------|
| `save_message()` | Save encrypted message with hashing |
| `get_service_messages()` | Retrieve messages for a service |
| `verify_message_integrity()` | Check message integrity |
| `get_database_stats()` | Get statistics |

**Features**:
- PostgreSQL integration
- Automatic BLAKE2s + SHA-3 hashing
- Message integrity verification
- Audit logging

---

### **4. `app/models.py`** (297 lines)

**Purpose**: SQLAlchemy database models

**Key Classes**:

#### **`QuantumSafeMessage`**
- Stores encrypted messages with quantum-safe hashing
- Fields: sender, receiver, encrypted data, signatures
- Automatic dual hashing (BLAKE2s + SHA-3)
- Integrity verification methods

#### **`MessageAuditLog`**
- Audit trail for all message operations
- BLAKE2s hash for tamper detection
- Tracks: create, verify, access operations

**Key Methods**:
| Method | Purpose |
|--------|---------|
| `_generate_quantum_safe_hashes()` | Generate BLAKE2s + SHA-3 hashes |
| `verify_integrity()` | Verify message hasn't been tampered |
| `to_dict()` | Convert to dictionary |
| `find_by_hash()` | Search by hash value |

---

### **5. `app/run.py`** (533 lines)

**Purpose**: Main Flask application and API routes

**Key Routes**:

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Homepage |
| `/demo` | GET | Algorithm demonstrations |
| `/tls` | GET | TLS demo page |
| `/messaging` | GET | Messaging interface |
| `/dashboard` | GET | System dashboard |
| `/api/demo/kem` | POST | Demonstrate KEM |
| `/api/demo/signature` | POST | Demonstrate signatures |
| `/api/demo/symmetric` | POST | Demonstrate encryption |
| `/api/messaging/send` | POST | Send encrypted message |
| `/api/messaging/history/<id>` | GET | Get message history |
| `/api/tls/*` | Various | TLS operations |
| `/api/database/messages` | GET | Get all messages |
| `/api/database/stats` | GET | Database statistics |

**Key Classes**:
- `QuantumSafeCrypto` - Demo utilities for web interface

---

### **6. `services/message_exchange_service.py`** (451 lines)

**Purpose**: Standalone quantum-safe messaging microservice

**Key Classes**:
- `QuantumSafeMessaging` - Message encryption/decryption

**Key Methods**:
| Method | Purpose |
|--------|---------|
| `generate_keypair()` | Generate RSA keys (PQ simulation) |
| `encrypt_message()` | Encrypt with AES-256-CBC |
| `decrypt_message()` | Decrypt and verify signature |
| `exchange_keys_with_partner()` | Key exchange protocol |

**API Endpoints**:
| Endpoint | Purpose |
|----------|---------|
| `/api/status` | Service health check |
| `/api/public-key` | Get service public key |
| `/api/key-exchange` | Initiate key exchange |
| `/api/send-message` | Send encrypted message |
| `/api/receive-message` | Receive and decrypt |
| `/api/message-history` | View message history |

---

## 🌐 API Endpoints Reference

### **TLS Management APIs**

```bash
# Get TLS certificate information
GET /api/tls/certificate-info

# Generate new post-quantum certificate
POST /api/tls/generate-certificate
{
    "domain": "example.com",
    "organization": "My Company",
    "validity_days": 365
}

# Get supported algorithms
GET /api/tls/supported-algorithms
```

---

### **Messaging APIs**

```bash
# Check messaging service status
GET /api/messaging/status

# Initiate key exchange between services
POST /api/messaging/initiate-key-exchange

# Send encrypted message
POST /api/messaging/send
{
    "message": "Secret message",
    "sender_service": "service-1"
}

# Get message history
GET /api/messaging/history/service-1
```

---

### **Algorithm Demonstration APIs**

```bash
# Demonstrate Key Encapsulation Mechanism
POST /api/demo/kem
{
    "algorithm": "Kyber768"
}

# Demonstrate Digital Signature
POST /api/demo/signature
{
    "algorithm": "Dilithium3",
    "message": "Sign this message"
}

# Demonstrate Symmetric Encryption
POST /api/demo/symmetric
{
    "algorithm": "ChaCha20-Poly1305",
    "message": "Encrypt this"
}
```

---

### **Database APIs**

```bash
# Get all messages from database
GET /api/database/messages?limit=50

# Get database statistics
GET /api/database/stats

# Get messages by hash
GET /api/database/messages/by-hash?hash=abc123&type=blake2
```

---

## 💾 Database Schema

### **Table: `quantum_safe_messages`**

| Column | Type | Purpose |
|--------|------|---------|
| `id` | Integer | Primary key |
| `sender_service_id` | String(50) | Sender identifier |
| `receiver_service_id` | String(50) | Receiver identifier |
| `message_type` | String(20) | Message category |
| `encrypted_message` | Text | Encrypted message content |
| `encrypted_key` | Text | Encrypted symmetric key |
| `initialization_vector` | String(256) | IV for decryption |
| `digital_signature` | Text | Message signature |
| `message_hash_blake2` | String(128) | BLAKE2s hash |
| `message_hash_sha3` | String(128) | SHA-3 hash |
| `content_hash` | String(128) | Content deduplication hash |
| `encryption_algorithm` | String(100) | Algorithm used |
| `key_exchange_algorithm` | String(100) | KEM used |
| `signature_algorithm` | String(100) | Signature algorithm |
| `created_at` | DateTime | Creation timestamp |
| `processed_at` | DateTime | Processing timestamp |
| `is_verified` | Boolean | Verification status |
| `verification_status` | String(50) | Status description |
| `message_metadata` | JSON | Additional metadata |

**Indexes**:
- `sender_service_id`
- `receiver_service_id`
- `message_hash_blake2`
- `message_hash_sha3`
- `created_at`

---

### **Table: `message_audit_logs`**

| Column | Type | Purpose |
|--------|------|---------|
| `id` | Integer | Primary key |
| `message_id` | Integer | Foreign key to messages |
| `operation` | String(50) | Operation type |
| `user_agent` | String(500) | Client user agent |
| `ip_address` | String(45) | Client IP address |
| `audit_hash` | String(128) | BLAKE2s audit hash |
| `created_at` | DateTime | Log timestamp |
| `context` | JSON | Additional context |

---

## 🚀 Deployment & Configuration

### **Docker Deployment**

```bash
# Start all services
docker-compose up -d

# Services started:
# - quantum-safe-web:5000 (Main application)
# - postgres:5432 (Database)
# - redis:6379 (Cache)
# - message-service-1:6000
# - message-service-2:6001
```

### **Environment Variables**

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `postgresql://quantum_user:...@postgres:5432/quantum_safe_db` | Database connection |
| `FLASK_ENV` | `development` | Flask environment |
| `OQS_PROVIDER_PATH` | `/usr/local/lib/ossl-modules/oqsprovider.so` | liboqs provider path |
| `SERVICE_ID` | `service-1` | Messaging service ID |

---

### **Configuration Files**

**`requirements.txt`** - Python dependencies:
- `Flask==2.3.3` - Web framework
- `pycryptodome==3.19.0` - Cryptography
- `cryptography==41.0.7` - Certificate management
- `psycopg2-binary==2.9.7` - PostgreSQL driver
- `pyoqs==0.9.0` (Optional) - Post-quantum crypto

**`docker-compose.yml`** - Multi-container setup:
- Web application container
- PostgreSQL database
- Redis cache
- Two messaging services (for demo)

---

## 🔍 Finding Specific Algorithms

### **Search by Algorithm Name**

| Algorithm | File Location | Line Numbers |
|-----------|---------------|--------------|
| **Kyber768** | `post_quantum_tls.py` | 49 |
| **Dilithium3** | `post_quantum_tls.py` | 60 |
| **ChaCha20-Poly1305** | `post_quantum_tls.py` | 332-342 |
| **AES-256-GCM** | `post_quantum_tls.py` | 344-352 |
| **BLAKE2s-256** | `models.py` | 94-130 |
| **SHA-3-256** | `models.py` | 94-130 |
| **RSA-OAEP** | `message_exchange_service.py` | 100-107 |
| **RSA-PSS** | `message_exchange_service.py` | 110-118 |

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser / Client                     │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS (Post-Quantum TLS)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Nginx Reverse Proxy (Port 80/443)               │
│                 + Post-Quantum TLS Termination               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│          Flask Web Application (Port 5000)                   │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   run.py     │  │ pq_tls_      │  │  database_   │      │
│  │ (API Routes) │──│  service.py  │──│  service.py  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                 │               │
│         │                  │                 │               │
│  ┌──────▼────────┐  ┌─────▼──────┐         │               │
│  │post_quantum_  │  │  models.py │         │               │
│  │   tls.py      │  │ (DB Models)│         │               │
│  │               │  │            │         │               │
│  │• Kyber768     │  │• BLAKE2s   │         │               │
│  │• Dilithium3   │  │• SHA-3     │         │               │
│  │• ChaCha20     │  │• Integrity │         │               │
│  └───────────────┘  └────────────┘         │               │
└────────────────────────────────────────────┼───────────────┘
                                              │
                      ┌───────────────────────┼───────────────┐
                      │                       │               │
                      ▼                       ▼               ▼
         ┌────────────────────┐  ┌────────────────┐  ┌──────────────┐
         │  PostgreSQL DB     │  │  Redis Cache   │  │Message       │
         │  (Port 5432)       │  │  (Port 6379)   │  │Services      │
         │                    │  │                │  │(Ports        │
         │• Encrypted msgs    │  │• Sessions      │  │ 6000-6001)   │
         │• Quantum hashes    │  │• Key cache     │  │              │
         │• Audit logs        │  │                │  │• Service-1   │
         └────────────────────┘  └────────────────┘  │• Service-2   │
                                                      └──────────────┘
```

---

## 🎓 Understanding the Algorithms in IT Context

### **Why Post-Quantum Cryptography?**

**The Threat**: Quantum computers using Shor's algorithm can break:
- RSA encryption
- Elliptic Curve Cryptography (ECC)
- Diffie-Hellman key exchange

**The Solution**: Post-quantum algorithms based on:
- **Lattice problems** (Kyber, Dilithium)
- **Hash functions** (SPHINCS+)
- **Code-based cryptography** (McEliece)
- **Multivariate equations** (Rainbow - not in this project)

---

### **IT Security Layers Using This Code**

1. **Transport Layer Security**
   - Replaces TLS 1.3 with post-quantum TLS
   - Protects data in transit
   - File: `pq_tls_service.py`

2. **Application Layer Encryption**
   - End-to-end message encryption
   - File: `message_exchange_service.py`

3. **Data Layer Protection**
   - Quantum-safe hashing for integrity
   - File: `models.py`

4. **Access Control**
   - Digital signatures for authentication
   - Key management for authorization
   - File: `post_quantum_tls.py`

---

## 📝 Quick Start for IT Professionals

### **1. Test the Application**

```bash
# Clone and start
cd QuantumSafeWebApplications
docker-compose up -d

# Access web interface
http://localhost:5000

# Test TLS endpoint
curl http://localhost:5000/api/tls/supported-algorithms

# Test messaging
curl -X POST http://localhost:5000/api/messaging/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Test", "sender_service": "service-1"}'
```

---

### **2. Integrate into Your Application**

```python
# Install dependencies
pip install -r requirements.txt

# Import post-quantum TLS
from post_quantum_tls import PostQuantumTLS, create_post_quantum_certificate_files

# Initialize
pq_tls = PostQuantumTLS(
    kem_algorithm='Kyber768',
    sig_algorithm='Dilithium3'
)

# Generate certificates
cert_file, key_file = create_post_quantum_certificate_files(
    domain="your-domain.com"
)

# Use in your application
ssl_context = pq_tls.create_secure_context(cert_file, key_file)
```

---

### **3. Monitor and Debug**

```bash
# Check logs
docker-compose logs -f quantum-safe-web

# Database access
docker-compose exec postgres psql -U quantum_user quantum_safe_db

# View messages
SELECT id, sender_service_id, encryption_algorithm, is_verified 
FROM quantum_safe_messages;

# Check audit logs
SELECT * FROM message_audit_logs ORDER BY created_at DESC LIMIT 10;
```

---

## 🔒 Security Best Practices

1. **Use Hybrid Mode**: Combine classical and post-quantum algorithms
2. **Key Rotation**: Regularly regenerate certificates (every 90 days)
3. **Audit Logging**: Monitor all cryptographic operations
4. **Hash Verification**: Use dual hashing (BLAKE2s + SHA-3)
5. **Secure Key Storage**: Protect private keys with proper permissions
6. **Regular Updates**: Keep liboqs and dependencies updated

---

## 📚 Additional Resources

- **NIST PQC Standardization**: https://csrc.nist.gov/projects/post-quantum-cryptography
- **liboqs Documentation**: https://github.com/open-quantum-safe/liboqs
- **BLAKE2 Specification**: https://www.blake2.net/
- **Kyber Algorithm**: https://pq-crystals.org/kyber/
- **Dilithium Algorithm**: https://pq-crystals.org/dilithium/

---

## 📞 Support & Contact

For questions or issues with this codebase:
1. Check the existing `README.md` for deployment instructions
2. Review `DEPLOYMENT_GUIDE.html` for detailed setup
3. Examine logs in `app/logs/` directory
4. Test individual algorithms using `/demo` page

---

**Last Updated**: February 2026
**Version**: 1.0
**Status**: Production-ready with simulation fallback
