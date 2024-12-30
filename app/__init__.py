# app/__init__.py

from flask import Flask
from .extensions import mongo, login_manager, mail, csrf, migrate, setup_logging
from .blueprints.auth import auth_bp
from .blueprints.errors import errors_bp, register_error_handlers
from .blueprints.main import main_bp  # Import main Blueprint

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, mongo)

    # Setup Logging
    setup_logging(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)    # Register main Blueprint
    app.register_blueprint(errors_bp)  # Register Errors Blueprint

    # Register Error Handlers
    register_error_handlers(app)

    # User Loader Callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.get(user_id)

    @app.context_processor
    def inject_environment():
        """Make the environment name (from config) available in all templates."""
        return {
            "current_environment": app.config.get("ENV_NAME", "Unknown")
        }

    return app