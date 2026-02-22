from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models.user_model import UserModel
from utils.security_utils import SecurityUtils
from utils.response_utils import ResponseUtils
from extensions.db import mongo

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'customer')
    
    if not all([username, email, password]):
        return ResponseUtils.error('All fields are required', 400)
    
    if UserModel.find_by_email(mongo.db, email):
        return ResponseUtils.error('Email already exists', 400)
    
    if UserModel.find_by_username(mongo.db, username):
        return ResponseUtils.error('Username already exists', 400)
    
    if role not in ['customer', 'officer', 'admin']:
        role = 'customer'
    
    password_hash = SecurityUtils.hash_password(password)
    
    user_id = UserModel.create_user(mongo.db, username, email, password_hash, role)
    
    return ResponseUtils.success(
        {'user_id': str(user_id), 'role': role},
        'User registered successfully',
        201
    )

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return ResponseUtils.error('Email and password are required', 400)
    
    user = UserModel.find_by_email(mongo.db, email)
    
    if not user:
        return ResponseUtils.error('Invalid credentials', 401)
    
    if not SecurityUtils.check_password(password, user['password']):
        return ResponseUtils.error('Invalid credentials', 401)
    
    access_token = create_access_token(identity=str(user['_id']))
    
    return ResponseUtils.success({
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    }, 'Login successful')