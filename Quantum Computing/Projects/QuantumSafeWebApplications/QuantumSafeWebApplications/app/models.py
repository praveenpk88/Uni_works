"""
Database models for quantum-safe message storage.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
import json
from typing import Dict, Any
from Cryptodome.Hash import BLAKE2s, SHA3_256

db = SQLAlchemy()

class QuantumSafeMessage(db.Model):
    """
    Model for storing quantum-safe encrypted messages with secure hashing.
    """
    __tablename__ = 'quantum_safe_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Message metadata
    sender_service_id = db.Column(db.String(50), nullable=False, index=True)
    receiver_service_id = db.Column(db.String(50), nullable=False, index=True)
    message_type = db.Column(db.String(20), default='standard', nullable=False)
    
    # Encrypted message data
    encrypted_message = db.Column(db.Text, nullable=False)
    encrypted_key = db.Column(db.Text, nullable=False)
    initialization_vector = db.Column(db.String(256), nullable=False)
    digital_signature = db.Column(db.Text, nullable=False)
    
    # Quantum-safe hashing
    message_hash_blake2 = db.Column(db.String(128), nullable=False, index=True)
    message_hash_sha3 = db.Column(db.String(128), nullable=False, index=True)
    content_hash = db.Column(db.String(128), nullable=False)
    
    # Cryptographic metadata
    encryption_algorithm = db.Column(db.String(100), nullable=False)
    key_exchange_algorithm = db.Column(db.String(100), nullable=False)
    signature_algorithm = db.Column(db.String(100), nullable=False)
    
    # Timestamps and audit trail
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    processed_at = db.Column(db.DateTime)
    
    # Message status and verification
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_status = db.Column(db.String(50), default='pending')
    
    # Additional metadata (JSON field for extensibility)
    message_metadata = db.Column(db.JSON)
    
    def __init__(self, sender_service_id: str, receiver_service_id: str, 
                 encrypted_data: Dict[str, Any], original_message: str = None):
        """
        Initialize a quantum-safe message record.
        
        Args:
            sender_service_id: ID of the sending service
            receiver_service_id: ID of the receiving service
            encrypted_data: Dictionary containing encrypted message data
            original_message: Original plaintext message (for hash verification)
        """
        self.sender_service_id = sender_service_id
        self.receiver_service_id = receiver_service_id
        
        # Store encrypted data
        self.encrypted_message = encrypted_data.get('encrypted_message', '')
        self.encrypted_key = encrypted_data.get('encrypted_key', '')
        self.initialization_vector = encrypted_data.get('iv', '')
        self.digital_signature = encrypted_data.get('signature', '')
        
        # Extract algorithm information
        algorithm_info = encrypted_data.get('algorithm', 'Unknown')
        self.encryption_algorithm = algorithm_info
        self.key_exchange_algorithm = 'RSA-OAEP (PQC Simulation)'
        self.signature_algorithm = 'RSA-PSS (PQC Simulation)'
        
        # Generate quantum-safe hashes
        self._generate_quantum_safe_hashes(encrypted_data, original_message)
        
        # Set metadata
        self.message_metadata = {
            'timestamp': encrypted_data.get('timestamp'),
            'message_size': len(self.encrypted_message),
            'key_size': len(self.encrypted_key),
            'signature_size': len(self.digital_signature)
        }
    
    def _generate_quantum_safe_hashes(self, encrypted_data: Dict[str, Any], original_message: str = None):
        """
        Generate multiple quantum-safe hashes for the message.
        
        Args:
            encrypted_data: Encrypted message data
            original_message: Original plaintext (if available)
        """
        # Combine all encrypted data for comprehensive hashing
        combined_data = json.dumps({
            'encrypted_message': encrypted_data.get('encrypted_message', ''),
            'encrypted_key': encrypted_data.get('encrypted_key', ''),
            'iv': encrypted_data.get('iv', ''),
            'sender_id': encrypted_data.get('sender_id', ''),
            'timestamp': encrypted_data.get('timestamp', '')
        }, sort_keys=True)
        
        # BLAKE2s hash (quantum-resistant)
        blake2_hasher = BLAKE2s.new()
        blake2_hasher.update(combined_data.encode('utf-8'))
        self.message_hash_blake2 = blake2_hasher.hexdigest()
        
        # SHA3-256 hash (quantum-resistant)
        sha3_hasher = SHA3_256.new()
        sha3_hasher.update(combined_data.encode('utf-8'))
        self.message_hash_sha3 = sha3_hasher.hexdigest()
        
        # Content hash (if original message is available)
        if original_message:
            content_hasher = BLAKE2s.new()
            content_hasher.update(original_message.encode('utf-8'))
            self.content_hash = content_hasher.hexdigest()
        else:
            # Hash the encrypted message as content
            content_hasher = BLAKE2s.new()
            content_hasher.update(self.encrypted_message.encode('utf-8'))
            self.content_hash = content_hasher.hexdigest()
    
    def verify_integrity(self, encrypted_data: Dict[str, Any], original_message: str = None) -> bool:
        """
        Verify the integrity of the message using quantum-safe hashes.
        
        Args:
            encrypted_data: Current encrypted message data
            original_message: Original plaintext message (if available)
            
        Returns:
            bool: True if integrity is verified, False otherwise
        """
        try:
            # Recreate hashes and compare
            temp_message = QuantumSafeMessage(
                self.sender_service_id, 
                self.receiver_service_id, 
                encrypted_data, 
                original_message
            )
            
            # Check BLAKE2 hash
            blake2_match = temp_message.message_hash_blake2 == self.message_hash_blake2
            
            # Check SHA3 hash
            sha3_match = temp_message.message_hash_sha3 == self.message_hash_sha3
            
            # Update verification status
            if blake2_match and sha3_match:
                self.is_verified = True
                self.verification_status = 'verified'
                self.processed_at = datetime.utcnow()
                return True
            else:
                self.verification_status = 'failed'
                return False
                
        except Exception as e:
            self.verification_status = f'error: {str(e)}'
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message record to a dictionary.
        
        Returns:
            dict: Dictionary representation of the message
        """
        return {
            'id': self.id,
            'sender_service_id': self.sender_service_id,
            'receiver_service_id': self.receiver_service_id,
            'message_type': self.message_type,
            'encryption_algorithm': self.encryption_algorithm,
            'message_hash_blake2': self.message_hash_blake2,
            'message_hash_sha3': self.message_hash_sha3,
            'content_hash': self.content_hash,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'is_verified': self.is_verified,
            'verification_status': self.verification_status,
            'message_metadata': self.message_metadata
        }
    
    @classmethod
    def find_by_hash(cls, hash_value: str, hash_type: str = 'blake3'):
        """
        Find messages by their quantum-safe hash.
        
        Args:
            hash_value: The hash value to search for
            hash_type: Type of hash ('blake3', 'sha3', or 'content')
            
        Returns:
            Query result for messages with matching hash
        """
        if hash_type == 'blake2':
            return cls.query.filter_by(message_hash_blake2=hash_value).all()
        elif hash_type == 'sha3':
            return cls.query.filter_by(message_hash_sha3=hash_value).all()
        elif hash_type == 'content':
            return cls.query.filter_by(content_hash=hash_value).all()
        else:
            return []
    
    @classmethod
    def get_service_messages(cls, service_id: str, message_type: str = None):
        """
        Get all messages for a specific service.
        
        Args:
            service_id: Service identifier
            message_type: Optional message type filter
            
        Returns:
            Query result for service messages
        """
        query = cls.query.filter(
            (cls.sender_service_id == service_id) | 
            (cls.receiver_service_id == service_id)
        )
        
        if message_type:
            query = query.filter_by(message_type=message_type)
        
        return query.order_by(cls.created_at.desc()).all()


class MessageAuditLog(db.Model):
    """
    Audit log for message operations with quantum-safe hashing.
    """
    __tablename__ = 'message_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('quantum_safe_messages.id'), nullable=False)
    
    # Audit information
    operation = db.Column(db.String(50), nullable=False)  # 'create', 'verify', 'access', etc.
    user_agent = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    
    # Quantum-safe audit trail hash
    audit_hash = db.Column(db.String(128), nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Additional context
    context = db.Column(db.JSON)
    
    def __init__(self, message_id: int, operation: str, context: Dict[str, Any] = None):
        """
        Initialize audit log entry.
        
        Args:
            message_id: ID of the message being audited
            operation: Type of operation performed
            context: Additional context information
        """
        self.message_id = message_id
        self.operation = operation
        self.context = context or {}
        
        # Generate audit hash
        self._generate_audit_hash()
    
    def _generate_audit_hash(self):
        """Generate quantum-safe hash for audit trail integrity."""
        audit_data = json.dumps({
            'message_id': self.message_id,
            'operation': self.operation,
            'timestamp': datetime.utcnow().isoformat(),
            'context': self.context
        }, sort_keys=True)
        
        # Use BLAKE2s for audit trail
        hasher = BLAKE2s.new()
        hasher.update(audit_data.encode('utf-8'))
        self.audit_hash = hasher.hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary."""
        return {
            'id': self.id,
            'message_id': self.message_id,
            'operation': self.operation,
            'audit_hash': self.audit_hash,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'context': self.context
        }