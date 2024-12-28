# app/__init__.py

from flask import Flask, render_template
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_wtf import CSRFProtect
from config import Config, TestConfig, DevelopmentConfig, ProductionConfig
from bson.objectid import ObjectId

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    """
    Application factory function.

    Args:
        config_class (Class): Configuration class to use for the Flask app.

    Returns:
        Flask app instance.
    """
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # Initialize extensions with app
    mongo.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'main.login'  # Redirects to login page if not authenticated

    # Register Blueprints
    from .routes import main_bp
    from .tasks import tasks_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp)

    # Register error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    """
    Registers custom error handlers for the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Local import to avoid circular dependencies
    try:
        oid = ObjectId(user_id)
    except Exception as e:
        return None
    user_data = mongo.db.users.find_one({'_id': oid})
    if user_data:
        return User(user_data)
    return None