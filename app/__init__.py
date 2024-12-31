# app/__init__.py

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .extensions import mongo, login_manager, mail, migrate, setup_logging
from .blueprints.auth import auth_bp
from .blueprints.errors import errors_bp, register_error_handlers
from .blueprints.main import main_bp
from .blueprints.user import user_bp

csrf = CSRFProtect()

def create_app(config_class):
    """
    Create and configure the Flask application.

    :param config_class: A config class (or string reference)
                         that defines app configuration.
    :return: The initialized Flask application instance.
    """
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
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    # Register Error Handlers
    register_error_handlers(app)


    @login_manager.user_loader
    def load_user(user_id):
        """
        User loader callback for Flask-Login.
        Loads a User by Mongo ObjectId string.
        """
        from .models.user import User
        return User.get(user_id)

    @app.context_processor
    def inject_environment():
        """
        Make the custom environment name (from config)
        available in all templates as 'current_environment'.
        """
        return {
            "current_environment": app.config.get("ENV_NAME", "Unknown")
        }

    return app