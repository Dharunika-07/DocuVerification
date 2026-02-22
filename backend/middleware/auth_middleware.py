# from functools import wraps
# from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
# from flask import jsonify
# from models.user_model import UserModel
# from extensions.db import mongo

# def jwt_required_custom(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         try:
#             verify_jwt_in_request()
#             return fn(*args, **kwargs)
#         except Exception as e:
#             return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
#     return wrapper

# def get_current_user():
#     user_id = get_jwt_identity()
#     return UserModel.find_by_id(mongo.db, user_id)

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from utils.response_utils import ResponseUtils
from extensions.db import mongo
from bson import ObjectId

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception:
            return ResponseUtils.error('Unauthorized', 401)
    return wrapper

def get_current_user():
    user_id = get_jwt_identity()
    return mongo.db.users.find_one({'_id': ObjectId(user_id)})
