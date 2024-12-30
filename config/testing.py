# config/testing.py
import os
from .base import BaseConfig

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    ENV_NAME = "Testing"
    WTF_CSRF_ENABLED = False  # Usually disabled for simpler test POSTs
    MONGO_URI = os.getenv("MONGO_URI_TEST", "mongodb://localhost:27017/efish_test_db")