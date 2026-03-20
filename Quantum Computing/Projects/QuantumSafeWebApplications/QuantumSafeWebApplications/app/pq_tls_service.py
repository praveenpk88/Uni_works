"""
Post-Quantum TLS Service for Flask Web Application.

This service provides TLS integration for the quantum-safe web application,
including certificate management, secure connections, and TLS handshake handling.
"""

import os
import ssl
import threading
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

from post_quantum_tls import pq_tls, create_post_quantum_certificate_files


class PostQuantumTLSService:
    """Service for managing Post-Quantum TLS in Flask applications."""
    
    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.certificates = {}
        self.tls_sessions = {}
        self.cert_dir = "/app/certs"
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize TLS service with Flask app."""
        self.app = app
        
        # Ensure certificate directory exists
        os.makedirs(self.cert_dir, exist_ok=True)
        
        # Generate or load post-quantum certificates
        self._setup_certificates()
        
        # Configure Flask for TLS
        self._configure_flask_tls()
        
        # Register TLS API routes
        self._register_tls_routes()
    
    def _setup_certificates(self):
        """Setup post-quantum TLS certificates."""
        try:
            # Generate certificates for localhost and the application
            domains = ['localhost', 'quantum-safe-app', 'quantum-safe-web']
            
            for domain in domains:
                cert_file = os.path.join(self.cert_dir, f"{domain}.crt")
                key_file = os.path.join(self.cert_dir, f"{domain}.key")
                
                if not (os.path.exists(cert_file) and os.path.exists(key_file)):
                    # Generate new post-quantum certificate
                    cert_path, key_path = create_post_quantum_certificate_files(
                        domain=domain,
                        output_dir=self.cert_dir
                    )
                    
                    self.certificates[domain] = {
                        'cert_file': cert_path,
                        'key_file': key_path,
                        'created_at': datetime.now().isoformat(),
                        'algorithm': pq_tls.kem_algorithm + " + " + pq_tls.sig_algorithm
                    }
                else:
                    # Load existing certificate
                    self.certificates[domain] = {
                        'cert_file': cert_file,
                        'key_file': key_file,
                        'loaded_at': datetime.now().isoformat()
                    }
                
                print(f"📜 Post-Quantum TLS certificate ready: {domain}")
                
        except Exception as e:
            print(f"❌ Certificate setup failed: {e}")
    
    def _configure_flask_tls(self):
        """Configure Flask application for TLS support."""
        if not self.app:
            return
        
        # Set TLS-related configuration
        self.app.config.update({
            'TLS_CERT_DIR': self.cert_dir,
            'TLS_ENABLED': True,
            'PQ_TLS_KEM': pq_tls.kem_algorithm,
            'PQ_TLS_SIGNATURE': pq_tls.sig_algorithm,
            'TLS_MODE': pq_tls.pq_mode
        })
    
    def _register_tls_routes(self):
        """Register TLS-related API routes."""
        if not self.app:
            return
        
        @self.app.route('/api/tls/info', methods=['GET'])
        def tls_info():
            """Get TLS configuration information."""
            return jsonify({
                'tls_enabled': True,
                'post_quantum_mode': pq_tls.pq_mode,
                'algorithms': pq_tls.get_supported_algorithms(),
                'active_kem': pq_tls.kem_algorithm,
                'active_signature': pq_tls.sig_algorithm,
                'certificates': [
                    {
                        'domain': domain,
                        'algorithm': info.get('algorithm', 'Unknown'),
                        'created_at': info.get('created_at', info.get('loaded_at'))
                    }
                    for domain, info in self.certificates.items()
                ],
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/tls/handshake', methods=['POST'])
        def tls_handshake():
            """Perform post-quantum TLS handshake."""
            try:
                data = request.get_json() or {}
                peer_public_key = data.get('public_key')
                role = data.get('role', 'server')
                
                if not peer_public_key:
                    return jsonify({'error': 'public_key required'}), 400
                
                # Perform post-quantum handshake
                handshake_result = pq_tls.perform_post_quantum_handshake(
                    peer_public_key, role
                )
                
                # Store session
                session_id = handshake_result['session_id']
                self.tls_sessions[session_id] = {
                    'handshake_result': handshake_result,
                    'created_at': datetime.now(),
                    'last_used': datetime.now()
                }
                
                return jsonify({
                    'success': True,
                    'handshake_result': handshake_result,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tls/encrypt', methods=['POST'])
        def tls_encrypt():
            """Encrypt message using post-quantum TLS session."""
            try:
                data = request.get_json() or {}
                message = data.get('message')
                session_id = data.get('session_id')
                shared_secret = data.get('shared_secret')
                
                if not message:
                    return jsonify({'error': 'message required'}), 400
                
                if not (session_id or shared_secret):
                    return jsonify({'error': 'session_id or shared_secret required'}), 400
                
                # Get shared secret from session if not provided
                if session_id and session_id in self.tls_sessions:
                    session = self.tls_sessions[session_id]
                    shared_secret = session['handshake_result']['shared_secret']
                    session['last_used'] = datetime.now()
                elif session_id and session_id not in self.tls_sessions:
                    return jsonify({'error': f'TLS session {session_id} not found'}), 404
                
                if not shared_secret:
                    return jsonify({'error': 'No shared secret available for encryption'}), 400
                
                # Encrypt message
                encrypted_data = pq_tls.encrypt_post_quantum_message(
                    message, shared_secret
                )
                
                return jsonify({
                    'success': True,
                    'encrypted_data': encrypted_data,
                    'session_id': session_id,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tls/decrypt', methods=['POST'])
        def tls_decrypt():
            """Decrypt message using post-quantum TLS session."""
            try:
                data = request.get_json() or {}
                encrypted_data = data.get('encrypted_data')
                session_id = data.get('session_id')
                shared_secret = data.get('shared_secret')
                
                if not encrypted_data:
                    return jsonify({'error': 'encrypted_data required'}), 400
                
                if not (session_id or shared_secret):
                    return jsonify({'error': 'session_id or shared_secret required'}), 400
                
                # Get shared secret from session if not provided
                if session_id and session_id in self.tls_sessions:
                    session = self.tls_sessions[session_id]
                    shared_secret = session['handshake_result']['shared_secret']
                    session['last_used'] = datetime.now()
                elif session_id and session_id not in self.tls_sessions:
                    return jsonify({'error': f'TLS session {session_id} not found'}), 404
                
                if not shared_secret:
                    return jsonify({'error': 'No shared secret available for decryption'}), 400
                
                # Decrypt message
                decrypted_message = pq_tls.decrypt_post_quantum_message(
                    encrypted_data, shared_secret
                )
                
                return jsonify({
                    'success': True,
                    'decrypted_message': decrypted_message,
                    'session_id': session_id,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/tls/sessions', methods=['GET'])
        def tls_sessions():
            """Get active TLS sessions."""
            active_sessions = []
            
            for session_id, session_data in self.tls_sessions.items():
                active_sessions.append({
                    'session_id': session_id,
                    'kem_algorithm': session_data['handshake_result']['kem_algorithm'],
                    'sig_algorithm': session_data['handshake_result']['sig_algorithm'],
                    'role': session_data['handshake_result']['role'],
                    'created_at': session_data['created_at'].isoformat(),
                    'last_used': session_data['last_used'].isoformat(),
                    'handshake_complete': session_data['handshake_result']['handshake_complete']
                })
            
            return jsonify({
                'success': True,
                'active_sessions': len(active_sessions),
                'sessions': active_sessions,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/tls/certificate/<domain>', methods=['GET'])
        def get_certificate(domain):
            """Get certificate information for a domain."""
            if domain not in self.certificates:
                return jsonify({'error': 'Certificate not found'}), 404
            
            cert_info = self.certificates[domain]
            cert_file = cert_info['cert_file']
            
            try:
                with open(cert_file, 'r') as f:
                    cert_content = f.read()
                
                return jsonify({
                    'success': True,
                    'domain': domain,
                    'certificate': cert_content,
                    'algorithm': cert_info.get('algorithm', 'Unknown'),
                    'created_at': cert_info.get('created_at'),
                    'cert_file': cert_file,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def get_ssl_context(self, domain: str = 'localhost') -> Optional[ssl.SSLContext]:
        """
        Get SSL context for a specific domain.
        
        Args:
            domain: Domain name for certificate lookup
            
        Returns:
            SSL context or None if certificate not found
        """
        if domain not in self.certificates:
            return None
        
        cert_info = self.certificates[domain]
        
        try:
            context = pq_tls.create_secure_context(
                cert_file=cert_info['cert_file'],
                key_file=cert_info['key_file']
            )
            return context
        except Exception as e:
            print(f"Failed to create SSL context for {domain}: {e}")
            return None
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old TLS sessions."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        expired_sessions = [
            session_id for session_id, session_data in self.tls_sessions.items()
            if session_data['last_used'] < cutoff_time
        ]
        
        for session_id in expired_sessions:
            del self.tls_sessions[session_id]
        
        if expired_sessions:
            print(f"🧹 Cleaned up {len(expired_sessions)} expired TLS sessions")


# Global TLS service instance
tls_service = PostQuantumTLSService()


def configure_post_quantum_tls(app: Flask) -> PostQuantumTLSService:
    """
    Configure post-quantum TLS for Flask application.
    
    Args:
        app: Flask application instance
        
    Returns:
        Configured TLS service
    """
    tls_service.init_app(app)
    
    # Start session cleanup thread
    def cleanup_thread():
        while True:
            time.sleep(3600)  # Run every hour
            tls_service.cleanup_old_sessions()
    
    cleanup_thread = threading.Thread(target=cleanup_thread, daemon=True)
    cleanup_thread.start()
    
    return tls_service