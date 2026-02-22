from functools import wraps
from flask import jsonify
from middleware.auth_middleware import get_current_user

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            if current_user['role'] not in allowed_roles:
                return jsonify({'success': False, 'message': 'Access denied'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator