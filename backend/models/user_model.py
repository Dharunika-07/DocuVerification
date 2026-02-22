from datetime import datetime
from bson import ObjectId

class UserModel:
    @staticmethod
    def create_user(db, username, email, password_hash, role):
        user = {
            'username': username,
            'email': email,
            'password': password_hash,
            'role': role,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db.users.insert_one(user)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(db, email):
        return db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(db, user_id):
        return db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def find_by_username(db, username):
        return db.users.find_one({'username': username})