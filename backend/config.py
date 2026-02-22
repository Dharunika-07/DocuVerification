# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/verizon_verification')
#     JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
#     JWT_ACCESS_TOKEN_EXPIRES = 86400
#     GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
#     UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
#     MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}



import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')

    # Mongo
    MONGO_URI = os.getenv(
        'MONGO_URI',
        'mongodb://localhost:27017/verizon_verification'
    )

    # JWT (THIS IS THE FIX)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # Uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
