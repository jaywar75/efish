# app/blueprints/errors/__init__.py

from flask import Blueprint
import os

errors_bp = Blueprint('errors', __name__, template_folder=os.path.join(os.pardir, 'templates', 'errors'))

from . import handlers

def register_error_handlers(app):
    from .handlers import handle_403, handle_404, handle_500
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)