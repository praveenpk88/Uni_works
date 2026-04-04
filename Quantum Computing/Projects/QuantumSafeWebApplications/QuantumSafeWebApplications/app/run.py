#!/usr/bin/env python3
"""
Quantum-Safe Web Application
A demonstration web application showcasing post-quantum cryptography features.
"""

import os
from flask import (Flask, render_template, request, jsonify, session, flash,
                   redirect, url_for)
from flask_cors import CORS
import secrets
import base64
from datetime import datetime, timedelta
import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

# Import database components
from database_service import database_service
from models import db

# Import Post-Quantum TLS components
from pq_tls_service import configure_post_quantum_tls

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', secrets.token_hex(32)),
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)

# Initialize database service
database_service.init_app(app)

# Initialize Post-Quantum TLS service
tls_service = configure_post_quantum_tls(app)

class QuantumSafeCrypto:
    """Quantum-safe cryptography utilities (demo version with classical crypto)."""
    
    @staticmethod
    def get_supported_kems():
        """Get list of supported Key Encapsulation Mechanisms."""
        # Mock data for demo - in production this would use liboqs
        return ["Kyber512", "Kyber768", "Kyber1024", "NTRU-HPS-2048-509", "NTRU-HRSS-701"]
    
    @staticmethod
    def get_supported_sigs():
        """Get list of supported Digital Signature schemes."""
        # Mock data for demo - in production this would use liboqs
        return ["Dilithium2", "Dilithium3", "Dilithium5", "Falcon-512", "Falcon-1024", "SPHINCS+-SHA256-128s"]
    
    @staticmethod
    def demonstrate_kem(algorithm="Kyber512"):
        """Demonstrate Key Encapsulation Mechanism (mock implementation)."""
        try:
            # This is a classical RSA example for demo purposes
            # In production, this would use actual post-quantum algorithms
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()
            
            # Mock shared secret
            shared_secret = secrets.token_bytes(32)
            
            # Encrypt the shared secret (this simulates KEM encapsulation)
            ciphertext = public_key.encrypt(
                shared_secret,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decrypt to verify (this simulates KEM decapsulation)
            decrypted_secret = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            public_key_pem = public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            )
            
            return {
                'algorithm': f"{algorithm} (Classical RSA Demo)",
                'success': shared_secret == decrypted_secret,
                'public_key_size': len(public_key_pem),
                'ciphertext_size': len(ciphertext),
                'shared_secret_size': len(shared_secret),
                'public_key': base64.b64encode(public_key_pem).decode('utf-8')[:100] + "...",
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8')[:100] + "...",
                'shared_secret': base64.b64encode(shared_secret).decode('utf-8')[:50] + "..."
            }
        except Exception as e:
            logger.error(f"KEM demonstration failed: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def demonstrate_signature(algorithm="Dilithium2"):
        """Demonstrate Digital Signature scheme (mock implementation)."""
        try:
            message = b"This is a test message for quantum-safe digital signature demonstration."
            
            # This is a classical RSA example for demo purposes
            # In production, this would use actual post-quantum signature algorithms
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()
            
            # Sign the message
            signature = private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # Verify the signature
            try:
                public_key.verify(
                    signature,
                    message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                is_valid = True
            except Exception:
                is_valid = False
            
            public_key_pem = public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            )
            
            return {
                'algorithm': f"{algorithm} (Classical RSA Demo)",
                'message': message.decode('utf-8'),
                'signature_valid': is_valid,
                'public_key_size': len(public_key_pem),
                'signature_size': len(signature),
                'public_key': base64.b64encode(public_key_pem).decode('utf-8')[:100] + "...",
                'signature': base64.b64encode(signature).decode('utf-8')[:100] + "..."
            }
        except Exception as e:
            logger.error(f"Signature demonstration failed: {str(e)}")
            return {'error': str(e)}

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'quantum_safe': True
    })

@app.route('/api/algorithms')
def get_algorithms():
    """Get supported quantum-safe algorithms."""
    try:
        kems = QuantumSafeCrypto.get_supported_kems()
        sigs = QuantumSafeCrypto.get_supported_sigs()
        
        return jsonify({
            'key_encapsulation_mechanisms': kems,
            'digital_signatures': sigs,
            'total_kems': len(kems),
            'total_sigs': len(sigs)
        })
    except Exception as e:
        logger.error(f"Failed to get algorithms: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo/kem', methods=['POST'])
def demo_kem():
    """Demonstrate Key Encapsulation Mechanism."""
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'Kyber512')
    
    result = QuantumSafeCrypto.demonstrate_kem(algorithm)
    return jsonify(result)

@app.route('/api/demo/signature', methods=['POST'])
def demo_signature():
    """Demonstrate Digital Signature."""
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'Dilithium2')
    
    result = QuantumSafeCrypto.demonstrate_signature(algorithm)
    return jsonify(result)

@app.route('/api/generate-keys', methods=['POST'])
def generate_keys():
    """Generate quantum-safe key pairs."""
    data = request.get_json() or {}
    kem_algo = data.get('kem_algorithm', 'Kyber512')
    sig_algo = data.get('sig_algorithm', 'Dilithium2')
    
    try:
        # Mock key generation for demo (in production would use actual PQC algorithms)
        kem_public_key = secrets.token_bytes(800)  # Typical Kyber512 public key size
        sig_public_key = secrets.token_bytes(1312)  # Typical Dilithium2 public key size
        
        # Store in session for demonstration
        session['kem_algorithm'] = kem_algo
        session['sig_algorithm'] = sig_algo
        session['key_generated'] = True
        
        return jsonify({
            'success': True,
            'kem_algorithm': f"{kem_algo} (Demo)",
            'sig_algorithm': f"{sig_algo} (Demo)",
            'kem_public_key_size': len(kem_public_key),
            'sig_public_key_size': len(sig_public_key),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Key generation failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/status', methods=['GET'])
def get_messaging_status():
    """Get status of messaging services."""
    try:
        import requests
        
        services_status = {}
        service_urls = {
            'service-1': 'http://message-service-1:6000',
            'service-2': 'http://message-service-2:6001'
        }
        
        for service_id, url in service_urls.items():
            try:
                response = requests.get(f"{url}/api/status", timeout=5)
                if response.status_code == 200:
                    services_status[service_id] = response.json()
                else:
                    services_status[service_id] = {'error': f'HTTP {response.status_code}'}
            except Exception as e:
                services_status[service_id] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'services': services_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/initiate-key-exchange', methods=['POST'])
def initiate_messaging_key_exchange():
    """Initiate key exchange between messaging services."""
    try:
        import requests
        
        # Trigger key exchange from service-1 to service-2
        response = requests.post('http://message-service-1:6000/api/key-exchange', timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'success': True,
                'message': 'Key exchange initiated successfully',
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Key exchange failed with status {response.status_code}'
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/send', methods=['POST'])
def send_message_via_service():
    """Send a message through the messaging service."""
    try:
        import requests
        
        data = request.get_json() or {}
        message = data.get('message')
        sender_service = data.get('sender_service', 'service-1')
        
        if not message:
            return jsonify({'error': 'message is required'}), 400
        
        service_name = 'message-service-1' if sender_service == 'service-1' else 'message-service-2'
        service_port = 6000 if sender_service == 'service-1' else 6001
        response = requests.post(
            f'http://{service_name}:{service_port}/api/send-message',
            json={'message': message},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Save message to database with quantum-safe hashing
            try:
                receiver_service = 'service-2' if sender_service == 'service-1' else 'service-1'
                
                saved_message = database_service.save_message(
                    sender_service_id=sender_service,
                    receiver_service_id=receiver_service,
                    encrypted_data=result.get('encrypted_data', {}),
                    original_message=message,
                    partner_response=result.get('partner_response', {})
                )
                
                # Add database info to response
                result['database_info'] = {
                    'message_id': saved_message.id,
                    'blake2_hash': saved_message.message_hash_blake2,
                    'sha3_hash': saved_message.message_hash_sha3,
                    'is_verified': saved_message.is_verified,
                    'stored_at': saved_message.created_at.isoformat() if saved_message.created_at else None
                }
                
                logger.info(f"Message saved to database with ID: {saved_message.id}")
                
            except Exception as db_error:
                logger.error(f"Database save failed: {db_error}")
                # Don't fail the request if database save fails
                result['database_info'] = {'error': 'Failed to save to database'}
            
            return jsonify({
                'success': True,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Message send failed with status {response.status_code}'
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/history/<service_id>', methods=['GET'])
def get_message_history(service_id):
    """Get message history for a specific service."""
    try:
        import requests
        
        service_name = 'message-service-1' if service_id == 'service-1' else 'message-service-2'
        service_port = 6000 if service_id == 'service-1' else 6001
        response = requests.get(f'http://{service_name}:{service_port}/api/message-history', timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'success': True,
                'service_id': service_id,
                'history': result,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to get history with status {response.status_code}'
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/database/messages/<service_id>', methods=['GET'])
def get_stored_messages(service_id):
    """Get stored messages for a service from the database."""
    try:
        limit = request.args.get('limit', 50, type=int)
        messages = database_service.get_service_messages(service_id, limit)
        
        return jsonify({
            'success': True,
            'service_id': service_id,
            'message_count': len(messages),
            'messages': messages,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/database/statistics', methods=['GET'])
def get_message_statistics():
    """Get database statistics for messages."""
    try:
        stats = database_service.get_message_statistics()
        return jsonify({
            'success': True,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/database/verify/<int:message_id>', methods=['POST'])
def verify_message_integrity(message_id):
    """Verify the integrity of a stored message."""
    try:
        data = request.get_json() or {}
        encrypted_data = data.get('encrypted_data', {})
        decrypted_message = data.get('decrypted_message')
        
        result = database_service.verify_message_integrity(
            message_id, encrypted_data, decrypted_message
        )
        
        return jsonify({
            'success': result.get('success', False),
            'verification_result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/database/search', methods=['GET'])
def search_messages_by_hash():
    """Search for messages by their quantum-safe hash."""
    try:
        hash_value = request.args.get('hash')
        hash_type = request.args.get('type', 'blake2')
        
        if not hash_value:
            return jsonify({'error': 'hash parameter is required'}), 400
        
        messages = database_service.search_by_hash(hash_value, hash_type)
        
        return jsonify({
            'success': True,
            'hash_value': hash_value,
            'hash_type': hash_type,
            'matches': len(messages),
            'messages': messages,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messaging/database/audit/<int:message_id>', methods=['GET'])
def get_message_audit_trail(message_id):
    """Get audit trail for a specific message."""
    try:
        audit_trail = database_service.get_audit_trail(message_id)
        
        return jsonify({
            'success': True,
            'message_id': message_id,
            'audit_entries': len(audit_trail),
            'audit_trail': audit_trail,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard showing quantum-safe cryptography status."""
    return render_template('dashboard.html')

@app.route('/demo')
def demo():
    """Interactive demonstration page."""
    return render_template('demo.html')

@app.route('/messaging')
def messaging():
    """Quantum-safe messaging demonstration page."""
    return render_template('messaging.html')

@app.route('/tls')
def tls_demo():
    """Post-quantum TLS demonstration page."""
    return render_template('tls.html')

@app.route('/docs')
def documentation():
    """Project documentation page."""
    return render_template('documentation.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Quantum-Safe Web Application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)