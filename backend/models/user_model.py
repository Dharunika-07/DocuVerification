from datetime import datetime
from bson import ObjectId
from extensions.db import mongo


class UserModel:

    @staticmethod
    def create_user(username, email, password_hash, role):
        user = {
            "username": username,
            "email": email,
            "password": password_hash,
            "role": role,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = mongo.db.users.insert_one(user)
        return result.inserted_id

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})