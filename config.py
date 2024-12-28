# config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'efish_jaywar75_dec2024')
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/efish_db')
    WTF_CSRF_ENABLED = True  # Enable CSRF in production enviros
    # Add other configurations as needed

class TestConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI_TEST', 'mongodb://localhost:27017/efish_test_db')
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing purposes

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Production-specific configurations