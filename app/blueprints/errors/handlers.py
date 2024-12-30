# app/blueprints/errors/handlers.py

from flask import render_template

def handle_403(error):
    return render_template('errors/403.html'), 403

def handle_404(error):
    return render_template('errors/404.html'), 404

def handle_500(error):
    return render_template('errors/500.html'), 500