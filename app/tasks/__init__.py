# app/tasks/__init__.py

from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__, template_folder='templates/tasks', static_folder='static')

from . import routes  # Import routes to register them with the Blueprint