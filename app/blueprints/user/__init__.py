# app/blueprints/user/__init__.py
from flask import Blueprint

user_bp = Blueprint(
    'user',
    __name__,
    template_folder='templates',
    url_prefix='/user'
)

from . import routes