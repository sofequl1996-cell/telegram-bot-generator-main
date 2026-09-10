from functools import wraps
from flask import request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

logger = logging.getLogger(__name__)

# Admin credentials (should be in environment variables)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH', generate_password_hash('admin123'))


def verify_admin_password(password: str) -> bool:
    """Verify admin password"""
    return check_password_hash(ADMIN_PASSWORD_HASH, password)


def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


def api_token_required(f):
    """Decorator to require API token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        expected_token = os.getenv('API_TOKEN')
        
        if not token or token != f'Bearer {expected_token}':
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    return decorated_function
