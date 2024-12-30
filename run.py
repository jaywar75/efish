# run.py

import os
from app import create_app
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

def choose_config():
    """Decide which config to use based on FLASK_CONFIG env var."""
    config_name = os.getenv("FLASK_CONFIG", "development").lower()

    if config_name == "production":
        return ProductionConfig
    elif config_name == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig

def main():
    config_class = choose_config()
    app = create_app(config_class)
    app.run(host='0.0.0.0', port=7777)

if __name__ == "__main__":
    main()