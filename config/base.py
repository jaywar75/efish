# config/base.py

import os

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/efish_db')
    # Common configurations