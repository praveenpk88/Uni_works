"""
Database service for quantum-safe message storage.
"""
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from models import db, QuantumSafeMessage, MessageAuditLog

class DatabaseService:
    """Service for handling quantum-safe message database operations."""
    
    def __init__(self, app=None):
        """Initialize the database service."""
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the database with the Flask app."""
        # Database configuration
        database_url = os.environ.get('DATABASE_URL', 
                                    'postgresql://quantum_user:quantum_pass@postgres:5432/quantum_safe_db')
        
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 10,
            'pool_recycle': 120,
            'pool_pre_ping': True
        }
        
        db.init_app(app)
        
        with app.app_context():
            try:
                # Create tables if they don't exist
                db.create_all()
                print("Database tables created successfully")
            except Exception as e:
                print(f"Database initialization error: {e}")
    
    def save_message(self, sender_service_id: str, receiver_service_id: str, 
                    encrypted_data: Dict[str, Any], original_message: str = None,
                    partner_response: Dict[str, Any] = None) -> QuantumSafeMessage:
        """
        Save an encrypted message to the database with quantum-safe hashing.
        
        Args:
            sender_service_id: ID of the sending service
            receiver_service_id: ID of the receiving service  
            encrypted_data: Dictionary containing encrypted message data
            original_message: Original plaintext message (for verification)
            partner_response: Response from receiving service
            
        Returns:
            QuantumSafeMessage: The saved message record
        """
        try:
            # Create message record
            message = QuantumSafeMessage(
                sender_service_id=sender_service_id,
                receiver_service_id=receiver_service_id,
                encrypted_data=encrypted_data,
                original_message=original_message
            )
            
            # Add partner response to metadata if available
            if partner_response:
                if not message.message_metadata:
                    message.message_metadata = {}
                message.message_metadata['partner_response'] = partner_response
                
                # If decryption was successful, verify integrity
                if (partner_response.get('success') and 
                    partner_response.get('decrypted_result', {}).get('decryption_success')):
                    
                    decrypted_message = partner_response['decrypted_result'].get('message')
                    if decrypted_message and message.verify_integrity(encrypted_data, decrypted_message):
                        message.is_verified = True
                        message.verification_status = 'verified'
            
            # Save to database
            db.session.add(message)
            db.session.commit()
            
            # Create audit log
            self._create_audit_log(message.id, 'create', {
                'sender': sender_service_id,
                'receiver': receiver_service_id,
                'algorithm': encrypted_data.get('algorithm'),
                'verified': message.is_verified
            })
            
            return message
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to save message: {str(e)}")
    
    def get_service_messages(self, service_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get messages for a specific service.
        
        Args:
            service_id: Service identifier
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        try:
            messages = QuantumSafeMessage.get_service_messages(service_id)[:limit]
            return [msg.to_dict() for msg in messages]
        except Exception as e:
            print(f"Error retrieving messages for {service_id}: {e}")
            return []
    
    def verify_message_integrity(self, message_id: int, 
                               encrypted_data: Dict[str, Any], 
                               decrypted_message: str = None) -> Dict[str, Any]:
        """
        Verify the integrity of a stored message.
        
        Args:
            message_id: ID of the message to verify
            encrypted_data: Current encrypted data
            decrypted_message: Decrypted message content
            
        Returns:
            Dictionary with verification results
        """
        try:
            message = QuantumSafeMessage.query.get(message_id)
            if not message:
                return {'success': False, 'error': 'Message not found'}
            
            # Verify integrity
            is_valid = message.verify_integrity(encrypted_data, decrypted_message)
            
            # Update database
            db.session.commit()
            
            # Create audit log
            self._create_audit_log(message_id, 'verify', {
                'result': 'valid' if is_valid else 'invalid',
                'verification_status': message.verification_status
            })
            
            return {
                'success': True,
                'is_valid': is_valid,
                'verification_status': message.verification_status,
                'blake2_hash': message.message_hash_blake2,
                'sha3_hash': message.message_hash_sha3,
                'content_hash': message.content_hash
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_by_hash(self, hash_value: str, hash_type: str = 'blake3') -> List[Dict[str, Any]]:
        """
        Search for messages by their quantum-safe hash.
        
        Args:
            hash_value: Hash value to search for
            hash_type: Type of hash (blake3, sha3, content)
            
        Returns:
            List of matching message dictionaries
        """
        try:
            messages = QuantumSafeMessage.find_by_hash(hash_value, hash_type)
            return [msg.to_dict() for msg in messages]
        except Exception as e:
            print(f"Error searching by hash: {e}")
            return []
    
    def get_message_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics for messages.
        
        Returns:
            Dictionary with statistics
        """
        try:
            total_messages = QuantumSafeMessage.query.count()
            verified_messages = QuantumSafeMessage.query.filter_by(is_verified=True).count()
            
            # Count messages by service
            service_stats = {}
            services = ['service-1', 'service-2']
            
            for service in services:
                sent = QuantumSafeMessage.query.filter_by(sender_service_id=service).count()
                received = QuantumSafeMessage.query.filter_by(receiver_service_id=service).count()
                service_stats[service] = {'sent': sent, 'received': received}
            
            # Recent message activity (last 24 hours)
            yesterday = datetime.now(timezone.utc).replace(tzinfo=None) - \
                       __import__('datetime').timedelta(days=1)
            recent_messages = QuantumSafeMessage.query.filter(
                QuantumSafeMessage.created_at >= yesterday
            ).count()
            
            return {
                'total_messages': total_messages,
                'verified_messages': verified_messages,
                'verification_rate': (verified_messages / total_messages * 100) if total_messages > 0 else 0,
                'service_statistics': service_stats,
                'recent_activity': recent_messages
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def _create_audit_log(self, message_id: int, operation: str, context: Dict[str, Any]):
        """
        Create an audit log entry.
        
        Args:
            message_id: ID of the message
            operation: Operation being performed
            context: Additional context information
        """
        try:
            audit_log = MessageAuditLog(
                message_id=message_id,
                operation=operation,
                context=context
            )
            
            db.session.add(audit_log)
            db.session.commit()
            
        except Exception as e:
            print(f"Error creating audit log: {e}")
            db.session.rollback()
    
    def get_audit_trail(self, message_id: int) -> List[Dict[str, Any]]:
        """
        Get audit trail for a specific message.
        
        Args:
            message_id: ID of the message
            
        Returns:
            List of audit log entries
        """
        try:
            logs = MessageAuditLog.query.filter_by(message_id=message_id)\
                                      .order_by(MessageAuditLog.created_at.desc()).all()
            return [log.to_dict() for log in logs]
        except Exception as e:
            print(f"Error retrieving audit trail: {e}")
            return []


# Global database service instance
database_service = DatabaseService()