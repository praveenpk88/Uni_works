-- Database initialization script for quantum-safe web applications
-- This script sets up the database schema for storing quantum-safe keys and certificates

-- Create database (if not exists, handled by docker-entrypoint-initdb.d)
-- CREATE DATABASE IF NOT EXISTS quantumsafe;

-- Use the database
\c quantumsafe;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Table for storing quantum-safe key pairs
CREATE TABLE IF NOT EXISTS quantum_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_name VARCHAR(255) NOT NULL,
    algorithm_type VARCHAR(50) NOT NULL, -- 'KEM' or 'SIGNATURE'
    algorithm_name VARCHAR(100) NOT NULL,
    public_key BYTEA NOT NULL,
    private_key BYTEA, -- Nullable for public-only storage
    key_size INTEGER NOT NULL,
    security_level INTEGER NOT NULL, -- NIST security levels (1, 3, 5)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Table for storing certificates
CREATE TABLE IF NOT EXISTS certificates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    certificate_name VARCHAR(255) NOT NULL,
    certificate_data BYTEA NOT NULL,
    certificate_format VARCHAR(20) DEFAULT 'PEM', -- PEM, DER, etc.
    subject_dn VARCHAR(500),
    issuer_dn VARCHAR(500),
    serial_number VARCHAR(100),
    not_before TIMESTAMP WITH TIME ZONE,
    not_after TIMESTAMP WITH TIME ZONE,
    signature_algorithm VARCHAR(100),
    is_quantum_safe BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Table for storing cryptographic operations log
CREATE TABLE IF NOT EXISTS crypto_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operation_type VARCHAR(50) NOT NULL, -- 'KEY_GENERATION', 'SIGNATURE', 'ENCRYPTION', etc.
    algorithm_name VARCHAR(100) NOT NULL,
    key_id UUID REFERENCES quantum_keys(id),
    operation_data JSONB DEFAULT '{}'::jsonb,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    execution_time_ms INTEGER,
    client_ip INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing system configuration
CREATE TABLE IF NOT EXISTS system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_quantum_keys_algorithm ON quantum_keys(algorithm_name);
CREATE INDEX IF NOT EXISTS idx_quantum_keys_created_at ON quantum_keys(created_at);
CREATE INDEX IF NOT EXISTS idx_quantum_keys_active ON quantum_keys(is_active) WHERE is_active = TRUE;

CREATE INDEX IF NOT EXISTS idx_certificates_not_after ON certificates(not_after);
CREATE INDEX IF NOT EXISTS idx_certificates_quantum_safe ON certificates(is_quantum_safe) WHERE is_quantum_safe = TRUE;

CREATE INDEX IF NOT EXISTS idx_crypto_operations_created_at ON crypto_operations(created_at);
CREATE INDEX IF NOT EXISTS idx_crypto_operations_algorithm ON crypto_operations(algorithm_name);
CREATE INDEX IF NOT EXISTS idx_crypto_operations_success ON crypto_operations(success);

CREATE INDEX IF NOT EXISTS idx_system_config_key ON system_config(config_key);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_quantum_keys_updated_at 
    BEFORE UPDATE ON quantum_keys 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_config_updated_at 
    BEFORE UPDATE ON system_config 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default system configuration
INSERT INTO system_config (config_key, config_value, description) VALUES
    ('default_kem_algorithm', 'Kyber512', 'Default Key Encapsulation Mechanism algorithm'),
    ('default_sig_algorithm', 'Dilithium2', 'Default Digital Signature algorithm'),
    ('max_key_age_days', '365', 'Maximum age for quantum-safe keys in days'),
    ('enable_audit_logging', 'true', 'Enable detailed audit logging for crypto operations'),
    ('supported_security_levels', '[1,3,5]', 'JSON array of supported NIST security levels')
ON CONFLICT (config_key) DO NOTHING;

-- Create a view for active quantum-safe algorithms
CREATE OR REPLACE VIEW active_algorithms AS
SELECT 
    algorithm_name,
    algorithm_type,
    COUNT(*) as key_count,
    AVG(key_size) as avg_key_size,
    MIN(security_level) as min_security_level,
    MAX(security_level) as max_security_level,
    MAX(created_at) as last_used
FROM quantum_keys 
WHERE is_active = TRUE 
GROUP BY algorithm_name, algorithm_type
ORDER BY algorithm_type, algorithm_name;

-- Create a function to cleanup old operations (for maintenance)
CREATE OR REPLACE FUNCTION cleanup_old_operations(days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM crypto_operations 
    WHERE created_at < (CURRENT_TIMESTAMP - INTERVAL '1 day' * days_to_keep);
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions to application user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO qsafe_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO qsafe_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO qsafe_user;

-- Success message
\echo 'Quantum-safe database schema initialized successfully!'