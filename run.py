# run.py

from app import create_app
import os

config_type = os.getenv('FLASK_CONFIG', 'Config')  # Default to 'Config' if not set

# Map configuration names to classes
config_classes = {
    'Config': 'config.Config',
    'TestConfig': 'config.TestConfig',
    'DevelopmentConfig': 'config.DevelopmentConfig',
    'ProductionConfig': 'config.ProductionConfig'
}

app = create_app(config_class=config_classes.get(config_type, 'config.Config'))

if __name__ == '__main__':
    app.run()