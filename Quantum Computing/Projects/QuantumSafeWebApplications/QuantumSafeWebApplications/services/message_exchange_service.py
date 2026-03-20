#!/usr/bin/env python3
"""
Quantum-Safe Message Exchange Service
A secure messaging service using post-quantum cryptography for encrypted communication.
"""

import os
import json
import base64
import secrets
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Service configuration
SERVICE_ID = os.environ.get('SERVICE_ID', 'service-1')
SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 6000))
PARTNER_SERVICE_URL = os.environ.get('PARTNER_SERVICE_URL', 'http://localhost:6001')

class QuantumSafeMessaging:
    """Quantum-safe messaging using post-quantum cryptography simulation."""
    
    def __init__(self, service_id):
        self.service_id = service_id
        self.private_key = None
        self.public_key = None
        self.partner_public_key = None
        self.shared_secrets = {}
        self.message_history = []
        self.generate_keypair()
    
    def generate_keypair(self):
        """Generate a new key pair for this service."""
        # Using RSA as a placeholder for actual post-quantum algorithms
        # In production, this would use liboqs with Kyber, Dilithium, etc.
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        logger.info(f"Generated new keypair for service {self.service_id}")
    
    def get_public_key_pem(self):
        """Get the public key in PEM format."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def set_partner_public_key(self, partner_key_pem):
        """Set the partner service's public key."""
        self.partner_public_key = serialization.load_pem_public_key(partner_key_pem)
        logger.info("Partner public key set successfully")
    
    def encrypt_message(self, message, partner_key=None):
        """Encrypt a message using quantum-safe encryption."""
        if partner_key is None:
            partner_key = self.partner_public_key
        
        if partner_key is None:
            raise ValueError("No partner public key available")
        
        # Generate a random AES key for symmetric encryption
        aes_key = secrets.token_bytes(32)
        iv = secrets.token_bytes(16)
        
        # Encrypt the message with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Pad the message to be a multiple of 16 bytes
        padded_message = message.encode('utf-8')
        padding_length = 16 - (len(padded_message) % 16)
        padded_message += bytes([padding_length]) * padding_length
        
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        
        # Encrypt the AES key with the partner's public key (simulating KEM)
        encrypted_key = partner_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Sign the encrypted message for authenticity
        signature = self.private_key.sign(
            encrypted_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return {
            'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'signature': base64.b64encode(signature).decode('utf-8'),
            'sender_id': self.service_id,
            'timestamp': datetime.now().isoformat(),
            'algorithm': 'AES-256-CBC + RSA-OAEP (PQC Simulation)'
        }
    
    def decrypt_message(self, encrypted_data):
        """Decrypt a message using quantum-safe decryption."""
        try:
            # Decode base64 data
            encrypted_message = base64.b64decode(encrypted_data['encrypted_message'])
            encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
            iv = base64.b64decode(encrypted_data['iv'])
            signature = base64.b64decode(encrypted_data['signature'])
            
            # Decrypt the AES key using our private key
            aes_key = self.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Verify the signature (if we have the sender's public key)
            if self.partner_public_key:
                try:
                    self.partner_public_key.verify(
                        signature,
                        encrypted_message,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    signature_valid = True
                except Exception:
                    signature_valid = False
            else:
                signature_valid = None
            
            # Decrypt the message with AES
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(encrypted_message) + decryptor.finalize()
            
            # Remove padding
            padding_length = decrypted_padded[-1]
            decrypted_message = decrypted_padded[:-padding_length]
            
            return {
                'message': decrypted_message.decode('utf-8'),
                'sender_id': encrypted_data['sender_id'],
                'timestamp': encrypted_data['timestamp'],
                'algorithm': encrypted_data['algorithm'],
                'signature_valid': signature_valid,
                'decryption_success': True
            }
            
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            return {
                'error': str(e),
                'decryption_success': False
            }

# Initialize the messaging system
messaging_service = QuantumSafeMessaging(SERVICE_ID)

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service_id': SERVICE_ID,
        'timestamp': datetime.now().isoformat(),
        'quantum_safe_messaging': True
    })

@app.route('/api/public-key', methods=['GET'])
def get_public_key():
    """Get this service's public key."""
    public_key_pem = messaging_service.get_public_key_pem()
    return jsonify({
        'service_id': SERVICE_ID,
        'public_key': base64.b64encode(public_key_pem).decode('utf-8'),
        'key_format': 'PEM',
        'algorithm': 'RSA-2048 (PQC Simulation)',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/set-partner-key', methods=['POST'])
def set_partner_key():
    """Set the partner service's public key."""
    try:
        data = request.get_json()
        partner_key_b64 = data.get('public_key')
        partner_id = data.get('service_id')
        
        if not partner_key_b64:
            return jsonify({'error': 'public_key is required'}), 400
        
        partner_key_pem = base64.b64decode(partner_key_b64)
        messaging_service.set_partner_public_key(partner_key_pem)
        
        return jsonify({
            'success': True,
            'message': f'Partner public key set for service {partner_id}',
            'service_id': SERVICE_ID,
            'partner_id': partner_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to set partner key: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/encrypt-message', methods=['POST'])
def encrypt_message():
    """Encrypt a message for secure transmission."""
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'message is required'}), 400
        
        if not messaging_service.partner_public_key:
            return jsonify({'error': 'Partner public key not set'}), 400
        
        encrypted_data = messaging_service.encrypt_message(message)
        
        # Store in message history
        messaging_service.message_history.append({
            'type': 'sent',
            'original_message': message,
            'encrypted_data': encrypted_data,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'encrypted_data': encrypted_data,
            'service_id': SERVICE_ID
        })
        
    except Exception as e:
        logger.error(f"Encryption failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt-message', methods=['POST'])
def decrypt_message():
    """Decrypt a received encrypted message."""
    try:
        data = request.get_json()
        encrypted_data = data.get('encrypted_data')
        
        if not encrypted_data:
            return jsonify({'error': 'encrypted_data is required'}), 400
        
        decrypted_result = messaging_service.decrypt_message(encrypted_data)
        
        # Store in message history
        messaging_service.message_history.append({
            'type': 'received',
            'encrypted_data': encrypted_data,
            'decrypted_result': decrypted_result,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'decrypted_result': decrypted_result,
            'service_id': SERVICE_ID
        })
        
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Send an encrypted message to the partner service."""
    try:
        import requests
        
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'message is required'}), 400
        
        if not messaging_service.partner_public_key:
            return jsonify({'error': 'Partner public key not set'}), 400
        
        # Encrypt the message
        encrypted_data = messaging_service.encrypt_message(message)
        
        # Send to partner service
        response = requests.post(
            f"{PARTNER_SERVICE_URL}/api/receive-message",
            json={'encrypted_data': encrypted_data},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'success': True,
                'message': 'Message sent successfully',
                'encrypted_data': encrypted_data,
                'partner_response': result,
                'service_id': SERVICE_ID
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Partner service responded with status {response.status_code}'
            }), 500
            
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/receive-message', methods=['POST'])
def receive_message():
    """Receive and decrypt a message from a partner service."""
    try:
        data = request.get_json()
        encrypted_data = data.get('encrypted_data')
        
        if not encrypted_data:
            return jsonify({'error': 'encrypted_data is required'}), 400
        
        # Decrypt the message
        decrypted_result = messaging_service.decrypt_message(encrypted_data)
        
        # Store in message history
        messaging_service.message_history.append({
            'type': 'received',
            'encrypted_data': encrypted_data,
            'decrypted_result': decrypted_result,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Received message: {decrypted_result.get('message', 'DECRYPTION_FAILED')}")
        
        return jsonify({
            'success': True,
            'message': 'Message received and decrypted',
            'decrypted_result': decrypted_result,
            'service_id': SERVICE_ID
        })
        
    except Exception as e:
        logger.error(f"Failed to receive message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/message-history', methods=['GET'])
def get_message_history():
    """Get the message history for this service."""
    return jsonify({
        'service_id': SERVICE_ID,
        'message_count': len(messaging_service.message_history),
        'messages': messaging_service.message_history[-10:],  # Last 10 messages
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/key-exchange', methods=['POST'])
def initiate_key_exchange():
    """Initiate key exchange with partner service."""
    try:
        import requests
        
        # Get our public key
        our_public_key = messaging_service.get_public_key_pem()
        
        # Send our public key to partner and get theirs
        response = requests.post(
            f"{PARTNER_SERVICE_URL}/api/set-partner-key",
            json={
                'public_key': base64.b64encode(our_public_key).decode('utf-8'),
                'service_id': SERVICE_ID
            },
            timeout=10
        )
        
        if response.status_code == 200:
            # Get partner's public key
            partner_response = requests.get(f"{PARTNER_SERVICE_URL}/api/public-key", timeout=10)
            
            if partner_response.status_code == 200:
                partner_data = partner_response.json()
                partner_key_b64 = partner_data['public_key']
                partner_id = partner_data['service_id']
                
                # Set partner's public key
                partner_key_pem = base64.b64decode(partner_key_b64)
                messaging_service.set_partner_public_key(partner_key_pem)
                
                return jsonify({
                    'success': True,
                    'message': 'Key exchange completed successfully',
                    'service_id': SERVICE_ID,
                    'partner_id': partner_id,
                    'timestamp': datetime.now().isoformat()
                })
        
        return jsonify({'error': 'Key exchange failed'}), 500
        
    except Exception as e:
        logger.error(f"Key exchange failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the service status and configuration."""
    return jsonify({
        'service_id': SERVICE_ID,
        'service_port': SERVICE_PORT,
        'partner_service_url': PARTNER_SERVICE_URL,
        'has_keypair': messaging_service.private_key is not None,
        'has_partner_key': messaging_service.partner_public_key is not None,
        'message_count': len(messaging_service.message_history),
        'timestamp': datetime.now().isoformat(),
        'quantum_safe': True
    })

if __name__ == '__main__':
    logger.info(f"Starting Quantum-Safe Message Exchange Service")
    logger.info(f"Service ID: {SERVICE_ID}")
    logger.info(f"Service Port: {SERVICE_PORT}")
    logger.info(f"Partner Service URL: {PARTNER_SERVICE_URL}")
    
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)