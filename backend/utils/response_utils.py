from flask import jsonify
from bson import ObjectId
from datetime import datetime

class ResponseUtils:
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        response = {
            'success': True,
            'message': message,
            'data': ResponseUtils.serialize(data) if data else None
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="Error", status_code=400, errors=None):
        response = {
            'success': False,
            'message': message,
            'errors': errors
        }
        return jsonify(response), status_code
    
    @staticmethod
    def serialize(obj):
        if isinstance(obj, list):
            return [ResponseUtils.serialize(item) for item in obj]
        elif isinstance(obj, dict):
            serialized = {}
            for key, value in obj.items():
                if isinstance(value, ObjectId):
                    serialized[key] = str(value)
                elif isinstance(value, datetime):
                    serialized[key] = value.isoformat()
                elif isinstance(value, (list, dict)):
                    serialized[key] = ResponseUtils.serialize(value)
                else:
                    serialized[key] = value
            return serialized
        return obj