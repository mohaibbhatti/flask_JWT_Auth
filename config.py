import os
from itsdangerous import URLSafeTimedSerializer

from dotenv import load_dotenv

# Ensure environment variables are loaded from .env file
load_dotenv()

class Configs:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2d4d5c9e0a7e4bfaec9e29c3de53b5b7398e9452e5c1db2f8a76d4f1c59c8c4d9'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'c8Q6n9tRf2Z8p7FNVu6hwv8j7B6J1Vxk6U9kHjMlL4a8b6g5e3c2a9s7f6e5d4'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://postgres:postgres@localhost/flask_db'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookies'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'lax'
    JWT_CSRF_IN_COOKIES = True
    WTF_CSRF_ENABLED = False

    @staticmethod
    def init_serializer():
        # Ensure SECRET_KEY is properly loaded
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY not found in environment variables")
        return URLSafeTimedSerializer(secret_key)
