# app/extensions.py

import logging
from logging.handlers import RotatingFileHandler
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

# Initialize Extensions
mongo = PyMongo()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
migrate = Migrate()

def setup_logging(app):
    if not app.debug and not app.testing:
        handler = RotatingFileHandler('error.log', maxBytes=100000, backupCount=10)
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)