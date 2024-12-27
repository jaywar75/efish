# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import DevelopmentConfig

mongo = PyMongo()
login_manager = LoginManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Redirects to login page if not authenticated

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app