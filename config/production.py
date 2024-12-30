# config/production.py

from .base import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV_NAME = "Production"
    # Production-specific configurations