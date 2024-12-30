# config/development.py
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV_NAME = 'Development'
    # You can override the MONGO_URI or anything else here if needed
    MONGO_URI = "mongodb://localhost:27017/efish_dev_db"